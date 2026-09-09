from mcp.server.fastmcp import FastMCP

from app.assets import asset_manifest, export_assets, list_assets, stats
from app.core.config import settings
from app.core.doctor import doctor
from app.db import history
from app.image.tools import *
from app.media.tools import (
    concat_videos,
    ffmpeg_status,
    media_probe,
    thumbnail_video,
    transcode_video,
    trim_video,
)
from app.providers.registry import provider_status
from app.video.tools import *

mcp = FastMCP("Bina", host=settings.host, port=settings.port, stateless_http=False)


@mcp.tool()
def bina_capabilities():
    return {
        "name": "Bina",
        "version": "0.7.0",
        "phase": "E",
        "features": [
            "asset_delivery",
            "secure_asset_resolution",
            "asset_preview",
            "asset_download",
            "asset_export",
            "asset_search",
            "media_pipeline",
            "persistent_jobs",
        ],
    }


@mcp.tool()
def bina_doctor():
    return doctor()


@mcp.tool()
def bina_provider_status():
    return provider_status()


@mcp.tool()
def bina_history(limit=50, status=None):
    return history(limit, status)


@mcp.tool()
def bina_asset_stats():
    return stats()


@mcp.tool()
def bina_list_assets(kind=None, limit=100, query=None):
    return list_assets(kind, limit, query)


@mcp.tool()
def bina_get_asset(asset_id):
    return asset_manifest(asset_id) or {"error": "asset_not_found"}


@mcp.tool()
def bina_export_assets(asset_ids: list[str]):
    p, items = export_assets(asset_ids)
    return {"path": str(p), "assets": items}


@mcp.tool()
def bina_ffmpeg_status():
    return ffmpeg_status()


for fn in (
    generate_image,
    edit_image,
    image_variation,
    upscale_image,
    remove_background,
    analyze_image,
    compare_images,
    generate_video,
    image_to_video,
    get_generation_status,
    get_generation_result,
    list_generation_jobs,
    cancel_generation,
    retry_generation,
    edit_video,
    extend_video,
    media_probe,
    transcode_video,
    trim_video,
    thumbnail_video,
    concat_videos,
):
    mcp.tool()(fn)
