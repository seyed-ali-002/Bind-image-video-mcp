from mcp.server.fastmcp import FastMCP
from app.core.config import settings
from app.image.tools import *
from app.video.tools import *
from app.storage.manager import storage
mcp=FastMCP('Bina',host=settings.host,port=settings.port,stateless_http=False)
@mcp.tool()
def bina_capabilities(): return {'name':'Bina','version':'0.1.0','features':['image_generation','image_editing','image_variation','image_upscale','background_removal','video_generation','image_to_video','video_editing','video_extension','async_jobs','asset_management']}
@mcp.tool()
def list_assets(kind='image'): return storage.list(kind)
@mcp.tool()
def delete_asset(kind,asset): return storage.delete(kind,asset)
for fn in (generate_image,edit_image,image_variation,upscale_image,remove_background,generate_video,image_to_video,get_generation_status,get_generation_result,edit_video,extend_video): mcp.tool()(fn)
