"""Shared discovery, reviewed explanations, and bilingual session handling."""

import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from threading import Lock
from uuid import uuid4

from src.models.evidence import ChatRequest, ChatResponse
from src.services.citations import ALLOCATION_NOTICE
from src.services.locality import financial_years, has_uncovered_location, normalize, resolve_localities, sector_for
from src.services.projects import get_coverage, search_projects
from src.services.explainer import definition, explain_project, glossary_term
from src.services.translator import NEXT_STEPS, REVIEW_CONTEXT, notice, translate
from src.services.verification import WORDING_REVIEWED, verify_claim, verification_message

SESSION_TTL = 30 * 60
PAGE_SIZE = 3


@dataclass
class Session:
    updated: float
    query: dict = field(default_factory=dict)
    result_ids: list[str] = field(default_factory=list)
    shown: int = 0
    language: str = "en"
    selected_id: str | None = None
    last_reply: tuple | None = None


class ConversationService:
    def __init__(self, db_path: Path, clock=time.monotonic):
        self.db_path = db_path
        self.clock = clock
        self.sessions: dict[str, Session] = {}
        self.lock = Lock()
        self.coverage = get_coverage(db_path)

    def reply(self, request: ChatRequest) -> ChatResponse:
        # A single POC process holds only bounded, short-lived anonymous context.
        with self.lock:
            now = self.clock()
            self.sessions = {key: value for key, value in self.sessions.items() if now - value.updated < SESSION_TTL}
            key = str(request.session_id) if request.session_id else str(uuid4())
            expired = request.session_id is not None and key not in self.sessions
            if expired:
                key = str(uuid4())
            if key not in self.sessions:
                if len(self.sessions) >= 1000:
                    oldest = min(self.sessions, key=lambda item: self.sessions[item].updated)
                    del self.sessions[oldest]
                self.sessions[key] = Session(updated=now)
            state = self.sessions[key]
            state.updated = now

            if request.language:
                state.language = request.language
            text = normalize(request.message)
            switching = request.action == "language" or text in {"sw", "kiswahili", "swahili", "en", "english", "kiingereza"}
            if text in {"sw", "kiswahili", "swahili"}:
                state.language = "sw"
            elif text in {"en", "english", "kiingereza"}:
                state.language = "en"
            elif re.match(r"^hakiki\b", text):
                # The Kiswahili verification command also chooses reply language,
                # including when the browser sends its previous EN preference.
                state.language = "sw"

            def respond(kind, message, **kwargs):
                state.last_reply = (kind, message, dict(kwargs))
                if kwargs.get("disclaimer"):
                    kwargs["disclaimer"] = notice(state.language)
                wording = message[state.language] if isinstance(message, dict) else translate(message, state.language)
                return ChatResponse(session_id=key, kind=kind, message=wording, coverage=self.coverage,
                                    language=state.language,
                                    review_context=REVIEW_CONTEXT[state.language] if kwargs.get("projects") else None,
                                    next_steps=NEXT_STEPS[state.language] if kwargs.get("projects") and kind in {"details", "explanation", "verification"} else None,
                                    review_notice=("Rasimu ya uhakiki; mapitio yanasubiriwa." if state.language == "sw" else "Draft verification wording; review pending.") if kind == "verification" and not WORDING_REVIEWED else None,
                                    **kwargs)

            if expired:
                return respond("expired", "Your conversation has expired. Select your ward or send your question again.", choices=self.coverage["wards"])
            if switching:
                if state.last_reply:
                    kind, message, kwargs = state.last_reply
                    return respond(kind, message, **kwargs)
                return respond("language", "English selected. Your current results are preserved.", choices=self.coverage["wards"])
            if text in {"french", "fr", "arabic", "spanish", "translate to french", "translate to arabic"}:
                return respond("unavailable", "Only English and Kiswahili are supported. Send EN or SW.")
            term = glossary_term(text)
            if term:
                en, sources = definition(term, "en")
                sw, _ = definition(term, "sw")
                return respond("explanation", {"en": en, "sw": sw}, explanation_sources=sources)
            if text in {"explain budget", "explain a budget term", "eleza bajeti"}:
                return respond("clarification", "Choose a budget term: allocation, recurrent expenditure, or development expenditure. Or select a project and send EXPLAIN.")
            if re.search(r"\b(verify|check|claim|true|false|someone|million|billion|ksh|kes|hakiki|kweli|uongo|milioni|bilioni)\b", text):
                # Verification never borrows the ward, year, or amount from a prior
                # discovery or claim. The user supplies the full comparison scope.
                state.query, state.result_ids, state.shown, state.selected_id = {}, [], 0, None
                checked = verify_claim(request.message, search_projects(self.db_path))
                state.result_ids = [p["id"] for p in checked["projects"]]
                state.shown = len(state.result_ids)
                return respond("verification", {lang: verification_message(checked, lang) for lang in ("en", "sw")},
                               projects=checked["projects"], verification={k: v for k, v in checked.items() if k != "projects"},
                               disclaimer=ALLOCATION_NOTICE if checked["projects"] else None)
            explaining = request.action == "explain" or bool(re.match(r"^(?:explain|eleza|fafanua)\b", text))
            selection = re.fullmatch(r"(?:explain|eleza|fafanua)(?:\s+(\d+))?", text)
            if request.action == "explain" or selection:
                selected = request.project_id or state.selected_id
                if selection and selection.group(1):
                    page_start = max(0, ((state.shown - 1) // PAGE_SIZE) * PAGE_SIZE)
                    page_ids = state.result_ids[page_start:state.shown]
                    index = int(selection.group(1)) - 1
                    selected = page_ids[index] if 0 <= index < len(page_ids) else None
                if selected not in state.result_ids[:state.shown]:
                    return respond("clarification", "Select a project first, then send EXPLAIN.", choices=self.coverage["wards"])
                results = search_projects(self.db_path, project_id=selected)
                state.selected_id = selected
                return respond("explanation", {lang: explain_project(results[0], lang) for lang in ("en", "sw")}, projects=results, disclaimer=ALLOCATION_NOTICE)
            if request.action == "coverage" or text in {"help", "coverage", "sources", "s", "msaada", "vyanzo"}:
                return respond("coverage", "The pilot covers fifteen reviewed allocation records in Wamagana, Mweiga, and Kabaru for FY 2026/2027. Only the programme budget supplies project answers; the second document is registered for later review.")
            if request.action == "more" or text in {"more", "next", "show more", "zaidi", "endelea"}:
                if not state.query:
                    return respond("clarification", "Choose a ward to start a project search.", choices=self.coverage["wards"])
                if state.shown >= len(state.result_ids):
                    return respond("empty", "You have reached the end of the matching records in our selected documents.")
                return self._page(state, respond)
            if request.action == "details" or text.isdigit():
                selected = request.project_id
                if text.isdigit():
                    page_start = max(0, ((state.shown - 1) // PAGE_SIZE) * PAGE_SIZE)
                    page_ids = state.result_ids[page_start:state.shown]
                    index = int(text) - 1
                    selected = page_ids[index] if 0 <= index < len(page_ids) else None
                if selected not in state.result_ids[:state.shown]:
                    return respond("clarification", "Select a project from your current results, or search by ward again.", choices=self.coverage["wards"])
                results = search_projects(self.db_path, project_id=selected)
                state.selected_id = selected
                return respond("details", "Here is the reviewed project record and its source.", projects=results, disclaimer=ALLOCATION_NOTICE)

            # Clear old pagination before interpreting a fresh question. Unsupported
            # queries must never silently reuse a previous area's records.
            state.query, state.result_ids, state.shown, state.selected_id = {}, [], 0, None
            if re.search(r"\b(spent|spending|expenditure|paid|completed|finished|built|procured|progress|zilitumika|imetumika|zimetumika|imelipwa|umekamilika|imekamilika|imejengwa|zimekamilika)\b", text):
                return respond("unavailable", "Not enough evidence to establish spending or completion. This pilot contains budget allocations only.", disclaimer=ALLOCATION_NOTICE)
            years = financial_years(text)
            bare_years = re.findall(r"\b20\d{2}\b", text)
            if len(years) > 1:
                return respond("clarification", "Please ask about one financial year at a time. Current coverage is FY 2026/2027.")
            if years and years[0] not in self.coverage["financial_years"]:
                return respond("empty", f"There are no reviewed records for FY {years[0]} in our coverage. We currently cover FY 2026/2027 only. This does not mean no projects exist.")
            if bare_years and not years:
                return respond("clarification", "Please specify the financial year, such as 2026/2027. A calendar year alone can span two financial years.")
            if has_uncovered_location(text, self.coverage):
                return respond("clarification", "I could not resolve that location within our pilot. Please choose Wamagana, Mweiga, or Kabaru in Nyeri County. Other places are outside current coverage.", choices=self.coverage["wards"])
            wards = resolve_localities(text, self.coverage)
            if len(wards) > 1:
                return respond("clarification", "Please choose one ward for this search.", choices=wards)

            # Exact source descriptions may identify a project, but duplicate names
            # such as 'Installation of streetlights' still need locality context.
            records = search_projects(self.db_path)
            named = [p for p in records if re.search(r"\b" + re.escape(normalize(p["name"])) + r"\b", text)]
            if named and wards:
                named = [p for p in named if p["ward"] == wards[0]]
            if len(named) == 1:
                state.result_ids, state.shown = [named[0]["id"]], 1
                state.selected_id = named[0]["id"]
                if explaining:
                    return respond("explanation", {lang: explain_project(named[0], lang) for lang in ("en", "sw")}, projects=named, disclaimer=ALLOCATION_NOTICE)
                return respond("details", "Here is the allocation recorded in the approved FY 2026/2027 budget.", projects=named, disclaimer=ALLOCATION_NOTICE)
            if len(named) > 1 and not wards:
                return respond("clarification", "That description appears in more than one ward. Which ward do you mean?", choices=sorted({p["ward"] for p in named}))
            if explaining:
                return respond("clarification", "That term is not in our glossary. Try allocation, recurrent expenditure, or development expenditure.")
            if ("how much" in text or "kiasi gani" in text) and not named:
                return respond("clarification", "I could not identify an exact project from that question. Search by ward and select a project to inspect its recorded allocation.", choices=self.coverage["wards"])
            if not wards:
                return respond("clarification", "Which ward in Nyeri County should I search? We cover selected records in Wamagana, Mweiga, and Kabaru only. An area outside this list is outside our current coverage.", choices=self.coverage["wards"])
            # Do not treat arbitrary instructions mentioning a locality as a query.
            if not (text in {normalize(wards[0]), normalize(wards[0]) + " ward"}
                    or re.search(r"\b(projects?|planned|allocat\w*|budget|show|find|roads?|school\w*|ecde|streetlights?|water|health|miradi|mradi|imepangwa|iliyopangwa|bajeti|onyesha|tafuta|barabara|shule|maji|afya|taa)\b", text)):
                return respond("clarification", "Try a question such as 'What projects are planned in Wamagana?' This version supports project discovery.", choices=self.coverage["wards"])
            state.query = {"county": "Nyeri", "ward": wards[0], "financial_year": "2026/2027", "sector": sector_for(text)}
            results = search_projects(self.db_path, **state.query)
            state.result_ids = [project["id"] for project in results]
            if not results:
                return respond("empty", f"No matching reviewed records for {wards[0]} in FY 2026/2027 were found in our selected documents. This does not mean no projects exist.", choices=self.coverage["wards"])
            return self._page(state, respond)

    def _page(self, state: Session, respond) -> ChatResponse:
        state.selected_id = None
        records = search_projects(self.db_path, **state.query)
        page = records[state.shown:state.shown + PAGE_SIZE]
        start = state.shown + 1
        state.shown += len(page)
        return respond("results", f"Showing {start}–{state.shown} of {len(records)} matching records for {state.query['ward']} in the approved FY 2026/2027 budget.",
                       projects=page, has_more=state.shown < len(records), disclaimer=ALLOCATION_NOTICE)
