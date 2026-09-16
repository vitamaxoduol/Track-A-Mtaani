import json

import pytest

from src.db.database import ROOT, connect
from src.db.seed import SEED_PATH, load_dataset, seed_database


def test_seed_is_reviewed_matches_processed_and_is_idempotent(tmp_path):
    assert SEED_PATH.read_bytes() == (ROOT / "data/processed/projects.json").read_bytes()
    db_path = tmp_path / "seed.sqlite3"
    assert seed_database(db_path) == seed_database(db_path) == 10
    with connect(db_path) as db:
        assert db.execute("SELECT COUNT(*) FROM observations").fetchone()[0] == 10
        assert db.execute("SELECT COUNT(*) FROM documents").fetchone()[0] == 2
    dataset = load_dataset()
    assert all(o.reviewer == "Project owner" for p in dataset.projects for o in p.observations)


@pytest.mark.parametrize("mutation", ["unreviewed", "missing_page", "wrong_amount", "wrong_source", "source_hash", "wrong_year", "float_amount", "duplicate_id", "zero_page"])
def test_import_rejects_invalid_evidence(tmp_path, mutation):
    data = json.loads(SEED_PATH.read_text())
    observation = data["projects"][0]["observations"][0]
    if mutation == "unreviewed": observation["review_status"] = "PENDING_HUMAN_REVIEW"
    elif mutation == "missing_page": del observation["source_pdf_page"]
    elif mutation == "wrong_amount": observation["amount_kes"] = "700000000.00"
    elif mutation == "wrong_source": observation["source_id"] = "unknown"
    elif mutation == "source_hash": data["sources"][0]["sha256"] = "0" * 64
    elif mutation == "wrong_year": observation["financial_year"] = "2025/2026"
    elif mutation == "float_amount": observation["amount_kes"] = 700000.0
    elif mutation == "duplicate_id": data["projects"][1]["id"] = data["projects"][0]["id"]
    elif mutation == "zero_page": observation["source_pdf_page"] = 0
    seed = tmp_path / "bad-seed.json"
    seed.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        seed_database(tmp_path / "bad.sqlite3", seed)


def test_search_real_reviewed_records(client):
    response = client.get("/api/v1/projects", params={"county": "nyeri", "ward": "wamagana", "financial_year": "2026/2027", "limit": 30})
    assert response.status_code == 200
    result = response.json()
    assert result["total"] == 6
    records = result["projects"]
    assert [p["observations"][0]["amount_kes"] for p in records] == ["700000.00", "700000.00", "700000.00", "1000000.00", "2000000.00", "3000000.00"]
    assert all(p["ward"] == "Wamagana" for p in records)
    assert all(o["amount_kind"] == "ALLOCATION" for p in records for o in p["observations"])


def test_filters_never_fall_back_to_all_projects(client):
    for params in [{"county": "Nairobi"}, {"ward": "Unknown"}, {"financial_year": "2025/2026"}, {"ward": "Mweiga", "sector": "water"}, {"ward": "' OR 1=1 --"}]:
        result = client.get("/api/v1/projects", params=params).json()
        assert result["projects"] == []
        assert result["total"] == 0
    assert client.get("/api/v1/projects", params={"sector": "roads"}).json()["total"] == 4


def test_details_and_coverage(client):
    record = client.get("/api/v1/projects/nyeri-2026-010").json()
    assert record["name"] == "Grading and Murraming"
    assert record["ward"] == "Kabaru"
    assert record["observations"][0]["formatted_amount"] == "KSh 2,500,000"
    assert client.get("/api/v1/projects/not-a-project").status_code == 404
    coverage = client.get("/api/v1/coverage").json()
    assert coverage["record_count"] == 10
    assert sum(s["used_for_answers"] for s in coverage["sources"]) == 1
    assert not coverage["features"]["whatsapp"]


def test_app_serves_frontend_without_exposing_raw_database(client):
    assert "Track-A-Mtaani" in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/data/track_mtaani.sqlite3").status_code == 404
    assert client.get("/.env").status_code == 404
    assert client.get("/api/v1/projects", params={"limit": 0}).status_code == 422
    assert client.get("/api/v1/projects", params={"offset": -1}).status_code == 422
