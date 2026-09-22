import pytest

from tests.test_intent import ask


def test_details_and_language_switch_keep_evidence_and_translate_guidance(client):
    result = ask(client, "Wamagana")
    assert result["review_context"] and result["next_steps"] is None
    key = result["session_id"]
    detail = ask(client, "2", session_id=key)
    assert "project name, ward, financial year, allocation and source page" in detail["next_steps"]
    assert "cannot establish either" in detail["next_steps"]
    assert "not current project progress" in detail["review_context"]
    sw = ask(client, "SW", session_id=key)
    assert sw["projects"] == detail["projects"]
    assert "Hatua inayofuata" in sw["next_steps"]
    assert "si maendeleo ya sasa" in sw["review_context"]
    explained = ask(client, "ELEZA", session_id=key)
    assert explained["next_steps"] == sw["next_steps"]
    en = ask(client, "EN", session_id=key)
    assert en["next_steps"] == detail["next_steps"]


@pytest.mark.parametrize("claim,verdict", [
    ("allocation KSh 3,000,000", "SUPPORTED"),
    ("allocation KSh 2,000,000", "CONTRADICTED_BY_AVAILABLE_SOURCE"),
    ("allocation KSh 3,000,000 and completed", "PARTIALLY_SUPPORTED"),
    ("spending KSh 3,000,000", "INSUFFICIENT_EVIDENCE"),
])
def test_verification_guidance_preserves_the_source_amount(client, claim, verdict):
    result = ask(client, "Verify Kianjogu Karaihu in Wamagana FY 2026/2027 approved " + claim)
    assert result["verification"]["verdict"] == verdict
    assert result["next_steps"]
    assert result["projects"][0]["observations"][0]["formatted_amount"] == "KSh 3,000,000"


@pytest.mark.parametrize("message", ["Nairobi", "HELP", "EXPLAIN allocation", "Verify unknown project"])
def test_no_project_does_not_get_record_dates_or_project_follow_up(client, message):
    result = ask(client, message)
    assert not result["projects"]
    assert result["review_context"] is None
    assert result["next_steps"] is None
