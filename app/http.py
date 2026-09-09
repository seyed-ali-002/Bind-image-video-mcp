from fastapi import FastAPI,Header
from app.core.config import settings
from app.core.security import authorize
from app.mcp.server import mcp
from app.core.doctor import doctor
from app.assets import stats
from app.db import history
app=FastAPI(title="Bina MCP Server",version="0.3.0")
@app.get("/health")
def health(): return {"status":"ok","service":"bina","version":"0.3.0"}
@app.get("/health/live")
def live(): return {"status":"alive"}
@app.get("/health/ready")
def ready(): return {"status":"ready","storage":stats()}
@app.get("/doctor")
def doctor_endpoint(): return doctor()
@app.get("/assets/stats")
def asset_stats(): return stats()
@app.get("/history")
def generation_history(limit:int=50): return history(limit)
@app.get("/connection")
def connection(authorization:str|None=Header(default=None)):
 authorize(authorization);return {"url":settings.connection_url,"token":settings.auth_token}
app.mount("/mcp",mcp.streamable_http_app())
