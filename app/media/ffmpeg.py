from __future__ import annotations
import shutil,subprocess
def available(): return bool(shutil.which("ffmpeg"))
def run(args):
 if not available(): raise RuntimeError("FFmpeg is not installed")
 return subprocess.run(["ffmpeg","-y",*args],check=True,capture_output=True,text=True).stdout
