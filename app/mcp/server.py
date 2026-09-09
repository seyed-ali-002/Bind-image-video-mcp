from mcp.server.fastmcp import FastMCP
from app.core.config import settings
from app.image.tools import *
from app.video.tools import *
from app.storage.manager import storage
from app.core.doctor import doctor
from app.assets import stats
from app.db import history
from app.media.ffmpeg import available
mcp=FastMCP("Bina",host=settings.host,port=settings.port,stateless_http=False)
@mcp.tool()
def bina_capabilities():
 return {"name":"Bina","version":"0.3.0","platforms":["linux","windows","macos"],"features":["multi_instance","installer","runner","doctor","sqlite_history","asset_management","image_generation","image_analysis","video_generation","async_jobs","ffmpeg"],"providers":{"image":settings.image_provider,"video":settings.video_provider}}
@mcp.tool()
def bina_doctor():return doctor()
@mcp.tool()
def bina_history(limit=50):return history(limit)
@mcp.tool()
def bina_asset_stats():return stats()
@mcp.tool()
def bina_ffmpeg_status():return {"available":available()}
@mcp.tool()
def list_assets(kind="image"):return storage.list(kind)
@mcp.tool()
def delete_asset(kind,asset):return storage.delete(kind,asset)
for fn in (generate_image,edit_image,image_variation,upscale_image,remove_background,analyze_image,compare_images,generate_video,image_to_video,get_generation_status,get_generation_result,edit_video,extend_video):mcp.tool()(fn)
