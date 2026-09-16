"""Signed Twilio Sandbox webhook. Disabled until explicitly configured.

Uses immediate TwiML replies and makes no outbound REST API calls. Live use
requires a Twilio account that permits custom replies; trial restrictions vary.
"""

import hashlib
import hmac
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qsl, urlparse
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, Response
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from src.db.database import connect
from src.models.evidence import ChatRequest, ChatResponse
from src.services.intent import SESSION_TTL, ConversationService

WEBHOOK_PATH = "/api/v1/whatsapp/webhook"
DEDUP_TTL = 24 * 60 * 60
FIRST_USE_NOTICE = (
    "Track-A-Mtaani is a POC using selected public documents. Messages pass through "
    "WhatsApp and Twilio. Avoid personal details. Temporary context expires after "
    "30 minutes. Reply HELP for coverage and privacy."
)


@dataclass(frozen=True)
class WhatsAppSettings:
    account_sid: str
    auth_token: str = field(repr=False)
    number: str
    webhook_url: str

    def __post_init__(self):
        url = urlparse(self.webhook_url)
        if not re.fullmatch(r"AC[0-9a-fA-F]{32}", self.account_sid):
            raise ValueError("TWILIO_ACCOUNT_SID must be a valid account SID")
        if not self.auth_token:
            raise ValueError("TWILIO_AUTH_TOKEN is required")
        if not re.fullmatch(r"whatsapp:\+[1-9]\d{6,14}", self.number):
            raise ValueError("TWILIO_WHATSAPP_NUMBER must use whatsapp:+countrycode format")
        if url.scheme != "https" or not url.hostname or url.path != WEBHOOK_PATH or url.query or url.fragment or url.username or url.password:
            raise ValueError("TWILIO_WEBHOOK_URL must be the exact public HTTPS webhook URL, without query or fragment")

    @classmethod
    def from_environment(cls):
        if os.environ.get("TRACK_MTAANI_WHATSAPP_ENABLED", "0") != "1":
            return None
        names = ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_WHATSAPP_NUMBER", "TWILIO_WEBHOOK_URL"]
        missing = [name for name in names if not os.environ.get(name)]
        if missing:
            raise ValueError("Missing WhatsApp configuration: " + ", ".join(missing))
        return cls(*(os.environ[name] for name in names))


def format_whatsapp(result: ChatResponse, first_use: bool = False) -> str:
    sw = result.language == "sw"
    def t(en, kiswahili):
        return kiswahili if sw else en
    paragraphs = [t(FIRST_USE_NOTICE, "Track-A-Mtaani ni jaribio lenye hati za umma zilizochaguliwa. Ujumbe hupitia WhatsApp na Twilio. Usitume taarifa binafsi. Muktadha huisha baada ya dakika 30. Tuma MSAADA.")] if first_use else []
    if result.review_notice:
        paragraphs.append(result.review_notice)
    paragraphs.append(result.message)
    sources = {}
    for index, project in enumerate(result.projects, 1):
        paragraphs.append(f"{index}. {project['name']}")
        for observation in project["observations"]:
            citation = observation["citation"]
            key = (citation["document_title"], citation["url"])
            sources.setdefault(key, len(sources) + 1)
            paragraphs.append(
                observation['formatted_amount'] + " " + t("allocated", "imetengwa") + "\n"
                + t(f"{project['ward']} Ward | FY {observation['financial_year']}", f"Wadi ya {project['ward']} | Mwaka wa fedha {observation['financial_year']}") + "\n"
                + t("Source", "Chanzo") + f" [{sources[key]}], PDF " + t("page", "ukurasa") + f" {citation['pdf_page']}"
            )
            if result.kind == "details":
                paragraphs.append(t("Department: ", "Idara: ") + project['department'] + "\n" + t("Evidence: ", "Ushahidi: ") + citation['excerpt'])
    for (title, url), index in sources.items():
        paragraphs.append(f"[{index}] {title}\n{url}")
    for source in result.explanation_sources:
        paragraphs.append(t("Definition source: ", "Chanzo cha maana: ") + source['title'] + "\nPDF " + t("page ", "ukurasa ") + str(source['pdf_page']) + "\n" + source['url'] + f"#page={source['pdf_page']}")
    # Project explanations already contain the caveat in their fixed wording.
    if result.disclaimer and result.kind != "explanation":
        paragraphs.append(result.disclaimer)
    if result.projects:
        paragraphs.append(t("Selected records only; not a complete ward budget.", "Rekodi zilizochaguliwa pekee; si bajeti nzima ya wadi."))
    if result.kind == "results":
        paragraphs.append(t(f"Reply 1–{len(result.projects)} for details.", f"Tuma 1–{len(result.projects)} kwa maelezo.") + (t(" MORE for the next results.", " ZAIDI kwa matokeo yanayofuata.") if result.has_more else ""))
    if result.kind == "details":
        paragraphs.append(t("Reply EXPLAIN for a plain-language explanation. SW / EN to switch language.", "Tuma ELEZA kwa maelezo rahisi. SW / EN kubadili lugha."))
    if result.choices:
        paragraphs.append(t("Reply with a ward name: ", "Tuma jina la wadi: ") + ", ".join(result.choices) + ".")
    if result.kind == "coverage":
        paragraphs.append(t("Messages pass through WhatsApp, Twilio, and this app. No AI provider is used. We keep temporary context for 30 minutes, and message IDs for 24 hours to prevent repeated processing. We do not persist raw numbers or message bodies. SW / EN to switch language; EXPLAIN allocation for a definition.", "Ujumbe hupitia WhatsApp, Twilio na programu hii. Hakuna mtoa huduma wa AI anayetumiwa. Tunahifadhi muktadha kwa dakika 30, na vitambulisho vya ujumbe kwa saa 24 kuzuia urudiaji. Hatuhifadhi nambari halisi au maandishi ya ujumbe. SW / EN kubadili lugha; ELEZA mgao wa bajeti kupata maana."))
        for source in result.coverage["sources"]:
            role = t("Answer source", "Chanzo cha majibu") if source["used_for_answers"] else t("Registered only", "Imesajiliwa pekee")
            paragraphs.append(f"{role}: {source['title']}\n{source['url']}")
    text = "\n\n".join(paragraphs)
    if len(text) > 1600:
        raise ValueError("WhatsApp reply exceeds the checked single-message limit")
    return text


class WhatsAppAdapter:
    def __init__(self, settings: WhatsAppSettings, conversation: ConversationService, db_path: Path, clock=time.time):
        self.settings = settings
        self.conversation = conversation
        self.db_path = db_path
        self.clock = clock
        self.validator = RequestValidator(settings.auth_token)
        self.senders: dict[str, tuple[str, float]] = {}
        self.lock = Lock()
        with connect(db_path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS whatsapp_receipts (message_id TEXT PRIMARY KEY, expires_at REAL NOT NULL)")

    def validate(self, form: FormData, signature: str) -> None:
        if not self.validator.validate(self.settings.webhook_url, form, signature):
            raise HTTPException(403, "Invalid webhook signature.")
        required = ["AccountSid", "MessageSid", "From", "To", "NumMedia"]
        if any(len(form.getlist(name)) != 1 for name in required) or len(form.getlist("Body")) > 1:
            raise HTTPException(400, "Missing or repeated webhook fields.")
        if form["AccountSid"] != self.settings.account_sid or form["To"] != self.settings.number:
            raise HTTPException(403, "Webhook account or recipient mismatch.")
        if not re.fullmatch(r"(?:SM|MM)[0-9a-fA-F]{32}", form["MessageSid"]):
            raise HTTPException(400, "Invalid message identifier.")
        # Twilio may supply a business-scoped user ID instead of a phone number.
        # Preserve the signed identifier unchanged for session hashing and replies.
        if not re.fullmatch(r"whatsapp:(?:\+[1-9][0-9]{6,14}|[A-Z]{2}\.[A-Za-z0-9]{1,128})", form["From"]) or form["From"] == form["To"]:
            raise HTTPException(400, "Invalid WhatsApp sender.")
        if not re.fullmatch(r"\d{1,2}", form["NumMedia"]):
            raise HTTPException(400, "Invalid media count.")

    def handle(self, form: FormData) -> str:
        with self.lock:
            now = self.clock()
            self.senders = {key: value for key, value in self.senders.items() if now - value[1] < SESSION_TTL}
            sender_key = hmac.new(self.settings.auth_token.encode(), form["From"].encode(), hashlib.sha256).hexdigest()
            prior = self.senders.get(sender_key)
            response = MessagingResponse()
            with connect(self.db_path) as db:
                db.execute("BEGIN IMMEDIATE")
                db.execute("DELETE FROM whatsapp_receipts WHERE expires_at <= ?", (now,))
                if db.execute("SELECT 1 FROM whatsapp_receipts WHERE message_id=?", (form["MessageSid"],)).fetchone():
                    return str(response)
                text = form.get("Body", "").strip()
                if int(form["NumMedia"]) or any(name in form for name in ("Latitude", "Longitude")):
                    reply = "Please send a text question with your ward name. Attachments, voice notes, and shared GPS locations are not supported by this POC."
                elif not text or len(text) > 1000:
                    reply = "Please send a text question of 1–1000 characters, such as 'What projects are planned in Wamagana?'"
                else:
                    # Clear stale mappings instead of consuming a resident's new
                    # question on a web-session expiration response.
                    session_id = prior[0] if prior and prior[0] in self.conversation.sessions else None
                    result = self.conversation.reply(ChatRequest(message=text, session_id=UUID(session_id) if session_id else None))
                    reply = format_whatsapp(result, first_use=prior is None)
                    if len(self.senders) >= 1000 and sender_key not in self.senders:
                        oldest = min(self.senders, key=lambda key: self.senders[key][1])
                        del self.senders[oldest]
                    self.senders[sender_key] = (result.session_id, now)
                response.message(reply)
                db.execute("INSERT INTO whatsapp_receipts VALUES (?, ?)", (form["MessageSid"], now + DEDUP_TTL))
            return str(response)


router = APIRouter()


@router.post(WEBHOOK_PATH, include_in_schema=False)
async def webhook(request: Request):
    adapter = request.app.state.whatsapp
    if adapter is None:
        raise HTTPException(503, "WhatsApp is not configured. Browser discovery is available.")
    if request.headers.get("content-type", "").split(";")[0].strip() != "application/x-www-form-urlencoded":
        raise HTTPException(415, "Expected a form-encoded webhook.")
    try:
        fields = parse_qsl((await request.body()).decode("utf-8", errors="strict"), keep_blank_values=True, max_num_fields=100)
    except (ValueError, UnicodeError):
        raise HTTPException(400, "Invalid webhook form.") from None
    form = FormData(fields)
    adapter.validate(form, request.headers.get("X-Twilio-Signature", ""))
    try:
        xml = await run_in_threadpool(adapter.handle, form)
    except ValueError:
        raise HTTPException(500, "Unable to format the response safely.") from None
    return Response(xml, media_type="application/xml")
