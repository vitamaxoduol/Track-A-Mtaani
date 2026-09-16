"""Import only reviewed records. Run with python -m src.db.seed."""

import hashlib
import json
from decimal import Decimal
from pathlib import Path

from src.db.database import ROOT, connect, default_db_path, initialize
from src.models.project import Dataset

SEED_PATH = ROOT / "data/seeds/demo_projects.json"


def load_dataset(seed_path: Path = SEED_PATH) -> Dataset:
    dataset = Dataset.model_validate_json(seed_path.read_text())
    documents = {source.id: source for source in dataset.sources}
    if len(documents) != len(dataset.sources):
        raise ValueError("Duplicate source IDs")
    for source in dataset.sources:
        path = (ROOT / source.local_path).resolve()
        if not path.is_relative_to((ROOT / "data/raw").resolve()):
            raise ValueError("Source snapshot must be within data/raw")
        if hashlib.sha256(path.read_bytes()).hexdigest() != source.sha256:
            raise ValueError(f"Source snapshot checksum mismatch: {source.id}")
    project_ids, observation_ids = set(), set()
    for project in dataset.projects:
        if project.id in project_ids:
            raise ValueError("Duplicate project ID")
        project_ids.add(project.id)
        for observation in project.observations:
            if observation.id in observation_ids:
                raise ValueError("Duplicate observation ID")
            observation_ids.add(observation.id)
            source = documents.get(observation.source_id)
            if not source or source.financial_year != observation.financial_year:
                raise ValueError("Observation source/year mismatch")
            if observation.source_pdf_page > (source.model_extra or {}).get("page_count", 10**6):
                raise ValueError("Source page is outside the document")
            # Pilot amounts are explicitly in Kshs., not thousands or millions.
            if Decimal(observation.original_amount.replace(",", "")) != Decimal(observation.amount_kes):
                raise ValueError("Original amount and normalized KES differ")
    return dataset


def seed_database(path: Path, seed_path: Path = SEED_PATH) -> int:
    dataset = load_dataset(seed_path)
    initialize(path)
    fingerprint = hashlib.sha256(seed_path.read_bytes()).hexdigest()
    with connect(path) as db:
        current = db.execute("SELECT value FROM metadata WHERE key='seed_sha256'").fetchone()
        if current and current[0] == fingerprint:
            return len(dataset.projects)
        # This database contains only the reviewed seed, never user chat history.
        db.execute("DELETE FROM observations")
        db.execute("DELETE FROM projects")
        db.execute("DELETE FROM documents")
        for source in dataset.sources:
            db.execute("INSERT INTO documents VALUES (?, ?)", (source.id, source.model_dump_json()))
        for project in dataset.projects:
            db.execute("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)",
                       (project.id, project.name, project.county, project.ward, project.department, project.spending_unit))
            for observation in project.observations:
                db.execute("INSERT INTO observations VALUES (?, ?, ?, ?, ?, ?)",
                           (observation.id, project.id, observation.source_id,
                            int(Decimal(observation.amount_kes) * 100), observation.financial_year,
                            observation.model_dump_json()))
        db.execute("INSERT OR REPLACE INTO metadata VALUES ('seed_sha256', ?)", (fingerprint,))
        db.execute("INSERT OR REPLACE INTO metadata VALUES ('coverage', ?)", (json.dumps(dataset.coverage),))
    return len(dataset.projects)


if __name__ == "__main__":
    count = seed_database(default_db_path())
    print(f"Imported {count} reviewed projects into {default_db_path()}")
