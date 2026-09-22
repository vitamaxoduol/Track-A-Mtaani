from src.services.citations import format_kes
from src.db.seed import load_dataset


def test_exact_money_formatting_including_cents_and_zero():
    assert format_kes(70000000) == "KSh 700,000"
    assert format_kes(101) == "KSh 1.01"
    assert format_kes(0) == "KSh 0"


def test_every_financial_observation_has_matching_readable_citation(client):
    records = client.get("/api/v1/projects", params={"limit": 30}).json()["projects"]
    for project in records:
        for observation in project["observations"]:
            cite = observation["citation"]
            assert cite["pdf_page"] in {278, 282, 287, 291, 292, 296}
            assert cite["printed_page"] == str(cite["pdf_page"])
            assert cite["page_url"] == cite["url"] + f"#page={cite['pdf_page']}"
            assert cite["url"].startswith("https://www.nyeri.go.ke/")
            assert "2026/2027" in cite["document_title"]
            assert "Estimated Budget amount (Kshs.)" == cite["amount_heading"]
            assert project["ward"] in cite["excerpt"]
            assert "not proof" in observation["disclaimer"]
    assert records[0]["observations"][0]["citation"]["pdf_page"] == 278
    assert records[9]["observations"][0]["citation"]["pdf_page"] == 292
    assert [(p["id"], p["observations"][0]["citation"]["pdf_page"]) for p in records[10:]] == [
        ("nyeri-2026-011", 291), ("nyeri-2026-012", 292), ("nyeri-2026-013", 292),
        ("nyeri-2026-014", 296), ("nyeri-2026-015", 282),
    ]


def test_citation_dates_preserve_each_records_manual_review_date(client):
    expected = {
        observation.id: observation.reviewed_date.isoformat()
        for project in load_dataset().projects for observation in project.observations
    }
    records = client.get("/api/v1/projects", params={"limit": 30}).json()["projects"]
    dates = set()
    for project in records:
        for observation in project["observations"]:
            date = observation["citation"]["reviewed_date"]
            assert date == expected[observation["id"]]
            dates.add(date)
    # Later additions must not inherit the initial review or PDF retrieval date.
    assert dates == {"2026-09-14", "2026-09-16"}
