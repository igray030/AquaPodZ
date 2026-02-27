import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_and_report_and_rollup_snapshot():
    csv_path = Path("sample_data/2025Q1.csv")
    with open(csv_path, "rb") as fh:
        res = client.post("/upload", params={"quarter": "2025Q1"}, files={"file": ("2025Q1.csv", fh, "text/csv")})
    assert res.status_code == 200

    rep = client.get("/reports/2025Q1")
    assert rep.status_code == 200
    payload = rep.json()
    assert "function" in payload and len(payload["function"]) > 0

    snap = client.get("/snapshots/2025Q1")
    assert snap.status_code == 200
    assert len(snap.json()["items"]) > 0
