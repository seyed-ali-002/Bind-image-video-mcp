from mcp.server.fastmcp import FastMCP
from app.core.config import settings
from app.image.tools import *
from app.video.tools import *
from app.core.doctor import doctor
from app.assets import stats,list_assets,get_asset
from app.db import history
from app.media.ffmpeg import available
from app.providers.registry import provider_status
mcp=FastMCP("Bina",host=settings.host,port=settings.port,stateless_http=False)
@mcp.tool()
def bina_capabilities():return {"name":"Bina","version":"0.5.0","phase":"C","features":["provider_architecture","openai_image","replicate_image","replicate_video","provider_health","persistent_jobs","assets"]}
@mcp.tool()
def bina_doctor():return doctor()
@mcp.tool()
def bina_provider_status():return provider_status()
@mcp.tool()
def bina_history(limit=50,status=None):return history(limit,status)
@mcp.tool()
def bina_asset_stats():return stats()
@mcp.tool()
def bina_list_assets(kind=None,limit=100):return list_assets(kind,limit)
@mcp.tool()
def bina_get_asset(asset_id):return get_asset(asset_id) or {"error":"asset_not_found"}
@mcp.tool()
def bina_ffmpeg_status():return {"available":available()}
for fn in (generate_image,edit_image,image_variation,upscale_image,remove_background,analyze_image,compare_images,generate_video,image_to_video,get_generation_status,get_generation_result,list_generation_jobs,cancel_generation,retry_generation,edit_video,extend_video):mcp.tool()(fn)
