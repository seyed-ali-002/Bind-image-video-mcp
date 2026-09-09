from __future__ import annotations
import shutil,sys
from pathlib import Path
from app.core.config import settings
from app.core.platform import info
from app.storage.manager import storage
from app.core.runtime import running,is_port_free
def doctor():
 checks={"python":sys.version_info>=(3,12),"storage":storage.root.exists(),"data_dir":Path(settings.data_dir).exists(),"port_available":bool(running()) or is_port_free(settings.port)}
 return {"healthy":all(checks.values()),"checks":checks,"python":sys.version.split()[0],"platform":info(),"ffmpeg":bool(shutil.which("ffmpeg")),"tailscale":bool(shutil.which("tailscale")),"image_provider":settings.image_provider,"video_provider":settings.video_provider}
