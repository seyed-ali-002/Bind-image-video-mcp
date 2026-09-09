from fastapi import FastAPI,Header,HTTPException
from app.core.config import settings
from app.core.security import authorize
from app.mcp.server import mcp
from app.core.doctor import doctor
from app.assets import stats,list_assets,get_asset,delete_asset
from app.db import history
from app.jobs.manager import list_jobs,get,serialize,cancel
from app.providers.registry import provider_status
from app.media.tools import media_probe,transcode_video,trim_video,thumbnail_video,concat_videos,ffmpeg_status
app=FastAPI(title="Bina MCP Server",version="0.6.0")
@app.get("/health")
def health():return {"status":"ok","service":"bina","version":"0.6.0"}
@app.get("/health/live")
def live():return {"status":"alive"}
@app.get("/health/ready")
def ready():return {"status":"ready","storage":stats(),"ffmpeg":ffmpeg_status()}
@app.get("/doctor")
def doctor_endpoint():return doctor()
@app.get("/providers")
def providers():return provider_status()
@app.get("/media/ffmpeg")
def media_ffmpeg():return ffmpeg_status()
@app.get("/media/probe/{source}")
def media_probe_endpoint(source:str):return media_probe(source)
@app.post("/media/transcode/{source}")
def media_transcode(source:str,crf:int=23):return {"job_id":transcode_video(source,crf)}
@app.post("/media/trim/{source}")
def media_trim(source:str,start:float=0,end:float|None=None):return {"job_id":trim_video(source,start,end)}
@app.post("/media/thumbnail/{source}")
def media_thumbnail(source:str,time:float=0):return {"job_id":thumbnail_video(source,time)}
@app.post("/media/concat")
def media_concat(sources:list[str]):return {"job_id":concat_videos(sources)}
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
