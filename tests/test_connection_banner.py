from app.core.connection import info


def test_connection_info_has_connector():
    data = info(mask_token=False)
    assert data["local_url"].endswith(str(data["port"]))
    assert data["local_mcp_url"].endswith("/mcp")
    assert "/mcp" in data["mcp_url"]
    assert data["custom_connector_url"].startswith("mcp://connector?")
    assert "token=" in data["custom_connector_url"]
