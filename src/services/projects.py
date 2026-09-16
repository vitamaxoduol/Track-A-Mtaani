"""Structured search of the reviewed pilot. No model or external requests."""

import json
from pathlib import Path

from src.db.database import connect
from src.services.citations import ALLOCATION_NOTICE, citation, format_kes


def get_coverage(path: Path) -> dict:
    with connect(path) as db:
        metadata = json.loads(db.execute("SELECT value FROM metadata WHERE key='coverage'").fetchone()[0])
        active_ids = {row[0] for row in db.execute("SELECT DISTINCT source_id FROM observations")}
        sources = [json.loads(row[0]) for row in db.execute("SELECT payload FROM documents ORDER BY id")]
        return {
            "county": metadata["county"], "wards": metadata["wards"],
            "financial_years": metadata["financial_years"],
            "record_count": db.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
            "gaps": metadata["gaps"], "statement": "Selected reviewed records only; this is not a complete ward or county project register.",
            "sources": [{"title": s["title"], "url": s["official_url"], "used_for_answers": s["id"] in active_ids} for s in sources],
            "features": {"discover": True, "whatsapp": False, "kiswahili": True, "explain": True, "verify": True},
        }


def search_projects(path: Path, *, county: str | None = None, ward: str | None = None,
                    financial_year: str | None = None, sector: str | None = None,
                    project_id: str | None = None) -> list[dict]:
    clauses, values = [], []
    for column, value in [("p.county", county), ("p.ward", ward), ("o.financial_year", financial_year), ("p.id", project_id)]:
        if value is not None:
            clauses.append(f"{column} = ? COLLATE NOCASE")
            values.append(value)
    if sector:
        clauses.append("p.spending_unit = ? COLLATE NOCASE")
        values.append({"roads": "Roads Headquarters", "education": "ECDE", "energy": "Energy", "water": "Water", "health": "Health"}[sector])
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    with connect(path) as db:
        rows = db.execute("""
            SELECT p.*, o.id AS observation_id, o.amount_minor, o.payload AS observation_payload,
                   d.payload AS source_payload
            FROM projects p JOIN observations o ON o.project_id=p.id
            JOIN documents d ON d.id=o.source_id
        """ + where + " ORDER BY p.id, o.id", values).fetchall()
    projects = {}
    for row in rows:
        observation, source = json.loads(row["observation_payload"]), json.loads(row["source_payload"])
        project = projects.setdefault(row["id"], {
            "id": row["id"], "name": row["name"], "county": row["county"], "ward": row["ward"],
            "department": row["department"], "spending_unit": row["spending_unit"], "observations": [],
        })
        project["observations"].append({
            "id": row["observation_id"], "amount_kes": observation["amount_kes"],
            "formatted_amount": format_kes(row["amount_minor"]), "amount_kind": observation["amount_kind"],
            "financial_year": observation["financial_year"], "approval_stage": observation["approval_stage"],
            "disclaimer": ALLOCATION_NOTICE, "citation": citation(source, observation),
        })
    return list(projects.values())
