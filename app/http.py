from fastapi import FastAPI,Header,HTTPException
from app.core.config import settings
from app.core.security import authorize
from app.mcp.server import mcp
from app.core.doctor import doctor
from app.assets import stats,list_assets,get_asset,delete_asset
from app.db import history
from app.jobs.manager import list_jobs,get,serialize,cancel
from app.providers.registry import provider_status
app=FastAPI(title="Bina MCP Server",version="0.5.0")
@app.get("/health")
def health():return {"status":"ok","service":"bina","version":"0.5.0"}
@app.get("/health/live")
def live():return {"status":"alive"}
@app.get("/health/ready")
def ready():return {"status":"ready","storage":stats()}
@app.get("/doctor")
def doctor_endpoint():return doctor()
@app.get("/providers")
def providers():return provider_status()
@app.get("/assets/stats")
def asset_stats():return stats()
@app.get("/assets")
def assets(kind:str|None=None,limit:int=100):return list_assets(kind,limit)
@app.get("/assets/{asset_id}")
def asset(asset_id:str):
 d=get_asset(asset_id)
 if not d:raise HTTPException(404,"asset_not_found")
 return d
@app.delete("/assets/{kind}/{asset_id}")
def asset_delete(kind:str,asset_id:str):return {"deleted":delete_asset(kind,asset_id)}
@app.get("/history")
def generation_history(limit:int=50,status:str|None=None):return history(limit,status)
@app.get("/jobs")
def jobs(limit:int=50,status:str|None=None):return list_jobs(limit,status)
@app.get("/jobs/{job_id}")
def job(job_id:str):
 d=serialize(get(job_id))
 if not d:raise HTTPException(404,"job_not_found")
 return d
@app.post("/jobs/{job_id}/cancel")
def job_cancel(job_id:str):return {"cancelled":cancel(job_id)}
@app.get("/connection")
def connection(authorization:str|None=Header(default=None)):
 authorize(authorization);return {"url":settings.connection_url,"token":settings.auth_token}
app.mount("/mcp",mcp.streamable_http_app())
