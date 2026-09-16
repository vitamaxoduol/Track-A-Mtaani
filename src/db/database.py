"""One SQLite file, parameterized queries, and separate financial observations."""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def default_db_path() -> Path:
    path = Path(os.environ.get("TRACK_MTAANI_DB_PATH", "data/track_mtaani.sqlite3"))
    return path if path.is_absolute() else ROOT / path


@contextmanager
def connect(path: Path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY, name TEXT NOT NULL, county TEXT NOT NULL,
                ward TEXT NOT NULL, department TEXT NOT NULL, spending_unit TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS observations (
                id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
                source_id TEXT NOT NULL REFERENCES documents(id),
                amount_minor INTEGER NOT NULL CHECK(amount_minor >= 0),
                financial_year TEXT NOT NULL, payload TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS project_location ON projects(county, ward);
            CREATE INDEX IF NOT EXISTS observation_project ON observations(project_id, financial_year);
            CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """)
