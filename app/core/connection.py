from __future__ import annotations

from urllib.parse import quote

from app.core.config import settings
from app.core.runtime import running


def _tailscale_url() -> str:
    try:
        from app.tailscale.connection import status

        data = status()
        peer = data.get("status", {}).get("Self", {})
        dns = peer.get("DNSName", "").rstrip(".")
        if dns:
            path = settings.public_path.strip("/")
            return f"https://{dns}/{path + '/' if path else ''}mcp"
    except Exception:
        pass
    return ""


def info(mask_token: bool = True):
    runtime = running() or {}
    port = runtime.get("port", settings.port)
    local = f"http://{settings.host}:{port}"
    local_mcp = f"{local}/mcp"
    public = settings.connection_url if settings.public_host else _tailscale_url()
    mcp_url = public or local_mcp
    token = settings.auth_token
    shown_token = token
    if mask_token and token:
        shown_token = f"{token[:6]}...{token[-4:]}"
    connector_url = (
        f"mcp://connector?url={quote(mcp_url, safe=':/?=&')}&"
        f"token={quote(token, safe='')}"
    )
    return {
        "status": "running" if runtime else "stopped",
        "local_url": local,
        "local_mcp_url": local_mcp,
        "mcp_url": mcp_url,
        "custom_connector_url": connector_url,
        "token": shown_token,
        "port": port,
    }
