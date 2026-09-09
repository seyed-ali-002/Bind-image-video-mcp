from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import settings
from app.http import app
from app.image.tools import generate_image
from app.video.tools import generate_video, get_generation_status

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_connection_auth():
    assert client.get("/connection").status_code == 401
    r = client.get(
        "/connection", headers={"Authorization": f"Bearer {settings.auth_token}"}
    )
    assert r.status_code == 200 and r.json()["url"].endswith("/mcp")


def test_image_generation():
    r = generate_image("test", 64, 64)
    assert Path(r["path"]).exists()


def test_video_job():
    job = generate_video("test", 1)
    import time

    for _ in range(20):
        s = get_generation_status(job)
        if s["status"] in ("completed", "failed"):
            break
        time.sleep(0.05)
    assert s["status"] == "completed" and s["result"]
