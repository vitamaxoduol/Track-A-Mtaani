from urllib.parse import urlencode
from xml.etree import ElementTree

import pytest
from fastapi.testclient import TestClient
from twilio.request_validator import RequestValidator

from src.api.whatsapp import WhatsAppAdapter, WhatsAppSettings
from src.db.database import connect
from src.main import create_app

# Synthetic credentials and numbers for local tests only; no Twilio API calls.
SETTINGS = WhatsAppSettings(
    account_sid="AC" + "1" * 32, auth_token="synthetic-test-token",
    number="whatsapp:+15005550006", webhook_url="https://example.test/api/v1/whatsapp/webhook",
)
PATH = "/api/v1/whatsapp/webhook"


@pytest.fixture
def wa_client(tmp_path, monkeypatch):
    monkeypatch.setenv("TRACK_MTAANI_WHATSAPP_ENABLED", "0")
    with TestClient(create_app(tmp_path / "wa.sqlite3", whatsapp_settings=SETTINGS)) as client:
        yield client


def fields(index=1, text="Wamagana", sender="whatsapp:+254700000001", **overrides):
    return {"AccountSid": SETTINGS.account_sid, "MessageSid": f"SM{index:032x}", "From": sender,
            "To": SETTINGS.number, "Body": text, "NumMedia": "0", **overrides}


def send(client, values, signature=None):
    signature = signature if signature is not None else RequestValidator(SETTINGS.auth_token).compute_signature(SETTINGS.webhook_url, values)
    return client.post(PATH, content=urlencode(values), headers={"Content-Type": "application/x-www-form-urlencoded", "X-Twilio-Signature": signature})


def reply_text(response):
    assert response.status_code == 200, response.text
    messages = ElementTree.fromstring(response.text).findall("Message")
    return "\n".join(message.text or "" for message in messages)


def test_disabled_by_default(client):
    assert client.post(PATH, data=fields()).status_code == 503


def test_signed_message_returns_same_evidence_as_browser(wa_client):
    body = reply_text(send(wa_client, fields(text="What projects are planned in Wamagana?")))
    records = wa_client.get("/api/v1/projects", params={"ward": "Wamagana"}).json()["projects"]
    for record in records:
        obs = record["observations"][0]
        assert record["name"] in body
        assert obs["formatted_amount"] in body
        assert str(obs["citation"]["pdf_page"]) in body
        assert obs["citation"]["document_title"] in body
        assert obs["citation"]["url"] in body
    assert "not proof" in body and "30 minutes" in body
    assert len(body) <= 1600
    assert "synthetic-test-token" not in body


def test_numbered_detail_and_pagination_keep_same_session(wa_client):
    send(wa_client, fields())
    detail = reply_text(send(wa_client, fields(2, "1")))
    assert "Hubuini ECDE" in detail and "Evidence:" in detail
    assert "700,000" in detail and len(detail) <= 1600
    assert "Record reviewed: 2026-09-14" in detail
    assert "Next step:" in detail and "not current project progress" in detail
    more = reply_text(send(wa_client, fields(3, "MORE")))
    assert "Kianjogu Karaihu" in more and "Showing 4–6" in more
    second = reply_text(send(wa_client, fields(4, "3")))
    assert "KSh 3,000,000" in second and "PDF page 291" in second


def test_duplicate_message_does_not_reply_or_advance_pagination(wa_client):
    send(wa_client, fields())
    first_more = fields(2, "MORE")
    assert "Showing 4–6" in reply_text(send(wa_client, first_more))
    duplicate = send(wa_client, first_more)
    assert reply_text(duplicate) == ""
    third = reply_text(send(wa_client, fields(3, "MORE")))
    assert "Showing 7–9" in third and "Kanyamati" in third
    assert "end of the matching" in reply_text(send(wa_client, fields(4, "MORE")))


def test_deduplication_survives_adapter_restart_and_retains_no_message_body(wa_client):
    send(wa_client, fields())
    previous = wa_client.app.state.whatsapp
    wa_client.app.state.whatsapp = WhatsAppAdapter(SETTINGS, previous.conversation, previous.db_path)
    assert reply_text(send(wa_client, fields())) == ""
    with connect(previous.db_path) as db:
        columns = [row[1] for row in db.execute("PRAGMA table_info(whatsapp_receipts)")]
        assert columns == ["message_id", "expires_at"]
        assert db.execute("SELECT COUNT(*) FROM whatsapp_receipts").fetchone()[0] == 1


def test_tampering_missing_signature_wrong_account_and_recipient(wa_client):
    original = fields()
    signature = RequestValidator(SETTINGS.auth_token).compute_signature(SETTINGS.webhook_url, original)
    assert send(wa_client, fields(text="Mweiga"), signature).status_code == 403
    assert send(wa_client, original, "").status_code == 403
    assert send(wa_client, fields(AccountSid="AC" + "2" * 32)).status_code == 403
    assert send(wa_client, fields(To="whatsapp:+15005550007")).status_code == 403
    assert wa_client.post(PATH, json=original).status_code == 415


def test_signature_includes_unfamiliar_provider_fields(wa_client):
    assert send(wa_client, fields(NewProviderField="included in signature")).status_code == 200


@pytest.mark.parametrize("sender", ["whatsapp:KE.ABC123xyz", "whatsapp:US." + "A" * 128])
def test_business_scoped_sender_can_discover_and_continue(wa_client, sender):
    assert "Hubuini ECDE" in reply_text(send(wa_client, fields(sender=sender)))
    assert "Showing 4–6" in reply_text(send(wa_client, fields(2, "MORE", sender=sender)))
    assert "Choose a ward" in reply_text(send(wa_client, fields(3, "MORE", sender="whatsapp:KE.DifferentUser")))
    original = fields(4, sender=sender)
    signature = RequestValidator(SETTINGS.auth_token).compute_signature(SETTINGS.webhook_url, original)
    assert send(wa_client, fields(4, sender="whatsapp:KE.TamperedUser"), signature).status_code == 403
    assert sender not in wa_client.app.state.whatsapp.senders


@pytest.mark.parametrize("overrides", [
    {"NumMedia": "-1"}, {"MessageSid": "not-a-sid"}, {"From": "someone@example.test"},
    {"From": "whatsapp:KE."}, {"From": "whatsapp:KE." + "A" * 129},
    {"From": "whatsapp:KEN.ABC123"}, {"From": "whatsapp:KE.ABC/123"},
    {"From": SETTINGS.number},
])
def test_malformed_signed_inputs_rejected(wa_client, overrides):
    assert send(wa_client, fields(**overrides)).status_code == 400


def test_media_and_gps_are_not_fetched_or_misrepresented(wa_client):
    body = reply_text(send(wa_client, fields(NumMedia="1", MediaUrl0="http://127.0.0.1/private")))
    assert "not supported" in body and "KSh" not in body
    body = reply_text(send(wa_client, fields(2, Latitude="-1", Longitude="36")))
    assert "not supported" in body


def test_long_or_blank_text_gets_helpful_reply(wa_client):
    assert "1–1000" in reply_text(send(wa_client, fields(text="x" * 1001)))
    assert "1–1000" in reply_text(send(wa_client, fields(2, "")))


def test_help_fits_limit_and_discloses_privacy_and_source_scope(wa_client):
    text = reply_text(send(wa_client, fields(text="HELP")))
    assert "24 hours" in text and "No AI provider" in text
    assert "Registered only" in text and len(text) <= 1600


def test_sender_sessions_are_separate_and_expire(wa_client):
    send(wa_client, fields())
    assert "Choose a ward" in reply_text(send(wa_client, fields(2, "MORE", sender="whatsapp:+254700000002")))
    adapter = wa_client.app.state.whatsapp
    adapter.clock = lambda: 10**12
    assert "Choose a ward" in reply_text(send(wa_client, fields(3, "MORE")))
    assert all(not key.startswith("whatsapp:") for key in adapter.senders)


def test_configuration_fails_clearly_without_exposing_token(monkeypatch):
    monkeypatch.setenv("TRACK_MTAANI_WHATSAPP_ENABLED", "1")
    for name in ["TWILIO_ACCOUNT_SID", "TWILIO_AUTH_TOKEN", "TWILIO_WHATSAPP_NUMBER", "TWILIO_WEBHOOK_URL"]:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(ValueError, match="Missing WhatsApp configuration"):
        WhatsAppSettings.from_environment()
    with pytest.raises(ValueError, match="exact public HTTPS"):
        WhatsAppSettings(SETTINGS.account_sid, SETTINGS.auth_token, SETTINGS.number, "http://localhost" + PATH)
    assert SETTINGS.auth_token not in repr(SETTINGS)


def test_signed_language_switch_and_explanation_preserve_session(wa_client):
    sender = 'whatsapp:KE.LanguageTest'
    first = reply_text(send(wa_client, fields(101, 'Wamagana', sender=sender)))
    sw = reply_text(send(wa_client, fields(102, 'SW', sender=sender)))
    assert 'Hubuini ECDE' in first and 'Hubuini ECDE' in sw
    assert 'KSh 700,000' in sw and 'imetengwa' in sw and 'Rekodi 1–3' in sw
    details = reply_text(send(wa_client, fields(103, '1', sender=sender)))
    assert 'Ushahidi:' in details
    assert 'Rekodi ilikaguliwa: 2026-09-14' in details
    assert 'Hatua inayofuata:' in details and 'si maendeleo ya sasa' in details
    explanation = reply_text(send(wa_client, fields(104, 'ELEZA', sender=sender)))
    assert 'si uthibitisho' in explanation and 'KSh 700,000' in explanation
    assert 'Rekodi 4–6' in reply_text(send(wa_client, fields(105, 'ZAIDI', sender=sender)))
    assert 'Showing 4–6' in reply_text(send(wa_client, fields(106, 'EN', sender=sender)))
    assert 'No AI provider' in reply_text(send(wa_client, fields(107, 'HELP', sender=sender)))


def test_signed_verification_and_language_switch(wa_client):
    claim = 'Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved allocation KSh 3 million'
    body = reply_text(send(wa_client, fields(201, claim)))
    assert 'Supported by the available source' in body
    assert 'KSh 3,000,000' in body and '291' in body
    assert 'Linaungwa mkono' in reply_text(send(wa_client, fields(202, 'SW')))
    body = reply_text(send(wa_client, fields(203, claim.replace('3 million', '2 million'))))
    assert 'Linapingwa na chanzo kilichopo' in body and 'KSh 2,000,000' in body
    assert 'KSh 3,000,000' in body
    assert reply_text(send(wa_client, fields(203, claim))) == ''


def test_hakiki_first_message_uses_kiswahili_without_language_setup(wa_client):
    text = 'Hakiki Kianjogu Karaihu katika Wamagana mwaka wa fedha 2026/2027 iliyoidhinishwa mgao KSh 3,000,000'
    body = reply_text(send(wa_client, fields(301, text, sender='whatsapp:KE.HakikiTest')))
    assert 'Linaungwa mkono na chanzo kilichopo' in body
    assert 'KSh 3,000,000' in body and 'imetengwa' in body
    assert 'PDF ukurasa 291' in body
    assert 'Track-A-Mtaani ni jaribio' in body
    assert 'Draft verification' not in body and 'Rasimu ya uhakiki' not in body
