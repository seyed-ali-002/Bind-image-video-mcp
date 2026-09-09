from __future__ import annotations
from app.core.config import settings
from app.core.runtime import running
def info(mask_token=True):
 r=running() or {};port=r.get("port",settings.port)
 host=settings.public_host or f"{settings.host}:{port}"
 url=settings.connection_url if settings.public_host else f"http://{host}/mcp"
 token=settings.auth_token
 if mask_token and token:token=token[:6]+"..."+token[-4:]
 return {"status":"running" if r else "stopped","local_url":f"http://{settings.host}:{port}","mcp_url":url,"token":token,"port":port}
