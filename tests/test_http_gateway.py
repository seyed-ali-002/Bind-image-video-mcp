from fastapi.testclient import TestClient

from app.core.config import settings
from app.http import app

client = TestClient(app)
AUTH = {"Authorization": f"Bearer {settings.auth_token}"}


def test_root_and_public_docs_are_reachable():
    assert client.get("/").status_code == 200
    assert client.get("/health").status_code == 200
    assert client.get("/docs").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_protected_routes_require_bearer_auth():
    assert client.get("/providers").status_code == 401
    assert client.get("/connection").status_code == 401
    assert client.get("/providers", headers=AUTH).status_code == 200
    assert client.get("/connection", headers=AUTH).status_code == 200


def test_mcp_endpoint_is_reachable_and_protected():
    assert client.get("/mcp").status_code == 401
    response = client.get("/mcp", headers=AUTH)
    assert response.status_code == 200
    assert response.json()["transport"] == "streamable-http"


def test_public_path_alias_reaches_same_routes():
    if not settings.public_path:
        return
    prefix = "/" + settings.public_path.strip("/")
    assert client.get(prefix + "/health").status_code == 200
    assert client.get(prefix + "/docs").status_code == 200
    assert client.get(prefix + "/providers", headers=AUTH).status_code == 200
