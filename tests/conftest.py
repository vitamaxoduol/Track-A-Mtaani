from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def client(tmp_path: Path):
    with TestClient(create_app(tmp_path / "test.sqlite3")) as test_client:
        yield test_client
