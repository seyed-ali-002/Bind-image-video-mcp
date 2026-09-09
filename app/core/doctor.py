from __future__ import annotations
import shutil,sys
from app.core.config import settings
from app.core.platform import info
from app.storage.manager import storage
def doctor():
 return {"python":sys.version.split()[0],"platform":info(),"data_dir":str(settings.data_dir),"storage":storage.root.exists(),"ffmpeg":bool(shutil.which("ffmpeg")),"tailscale":bool(shutil.which("tailscale")),"image_provider":settings.image_provider,"video_provider":settings.video_provider}
