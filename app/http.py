from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse

from app.api_models import ExportRequest
from app.assets import (
    asset_file,
    asset_manifest,
    delete_asset,
    export_assets,
    list_assets,
    stats,
)
from app.core.config import settings
from app.core.doctor import doctor
from app.core.security import authorize
from app.db import history
from app.jobs.manager import cancel, get, list_jobs, serialize
from app.mcp.server import mcp
from app.media.tools import (
    concat_videos,
    ffmpeg_status,
    media_probe,
    thumbnail_video,
    transcode_video,
    trim_video,
)
from app.providers.registry import provider_status

app = FastAPI(title="Bina MCP Server", version="0.7.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "bina", "version": "0.7.0"}


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready", "storage": stats(), "ffmpeg": ffmpeg_status()}


@app.get("/doctor")
def doctor_endpoint():
    return doctor()


@app.get("/providers")
def providers():
    return provider_status()


@app.get("/media/ffmpeg")
def media_ffmpeg():
    return ffmpeg_status()


@app.get("/media/probe/{source}")
def media_probe_endpoint(source: str):
    return media_probe(source)


@app.post("/media/transcode/{source}")
def media_transcode(source: str, crf: int = 23):
    return {"job_id": transcode_video(source, crf)}


@app.post("/media/trim/{source}")
def media_trim(source: str, start: float = 0, end: float | None = None):
    return {"job_id": trim_video(source, start, end)}


@app.post("/media/thumbnail/{source}")
def media_thumbnail(source: str, time: float = 0):
    return {"job_id": thumbnail_video(source, time)}


@app.post("/media/concat")
def media_concat(sources: list[str]):
    return {"job_id": concat_videos(sources)}


@app.get("/assets/stats")
def asset_stats():
    return stats()


@app.get("/assets")
def assets(kind: str | None = None, limit: int = 100, query: str | None = None):
    return list_assets(kind, limit, query)


@app.get("/assets/{asset_id}")
def asset(asset_id: str):
    d = asset_manifest(asset_id)
    if not d:
        raise HTTPException(404, "asset_not_found")
    return d


@app.get("/assets/{asset_id}/download")
def asset_download(asset_id: str):
    d, p = asset_file(asset_id)
    if not d:
        raise HTTPException(404, "asset_not_found")
    if not p:
        raise HTTPException(410, "asset_file_missing")
    return FileResponse(
        p, media_type=asset_manifest(asset_id)["content_type"], filename=d["name"]
    )


@app.get("/assets/{asset_id}/preview")
def asset_preview(asset_id: str):
    d, p = asset_file(asset_id)
    if not d:
        raise HTTPException(404, "asset_not_found")
    if not p:
        raise HTTPException(410, "asset_file_missing")
    return FileResponse(
        p,
        media_type=asset_manifest(asset_id)["content_type"],
        filename=d["name"],
        content_disposition_type="inline",
    )


@app.post("/assets/export")
def asset_export(body: ExportRequest):
    p, items = export_assets(body.asset_ids)
    return FileResponse(
        p,
        media_type="application/zip",
        filename="bina-assets.zip",
        headers={"X-Bina-Assets": str(len(items))},
    )


@app.delete("/assets/{kind}/{asset_id}")
def asset_delete(kind: str, asset_id: str):
    return {"deleted": delete_asset(kind, asset_id)}


@app.get("/history")
def generation_history(limit: int = 50, status: str | None = None):
    return history(limit, status)


@app.get("/jobs")
def jobs(limit: int = 50, status: str | None = None):
    return list_jobs(limit, status)


@app.get("/jobs/{job_id}")
def job(job_id: str):
    d = serialize(get(job_id))
    if not d:
        raise HTTPException(404, "job_not_found")
    return d


@app.post("/jobs/{job_id}/cancel")
def job_cancel(job_id: str):
    return {"cancelled": cancel(job_id)}


@app.get("/connection")
def connection(authorization: str | None = Header(default=None)):
    authorize(authorization)
    return {"url": settings.connection_url, "token": settings.auth_token}


app.mount("/mcp", mcp.streamable_http_app())
