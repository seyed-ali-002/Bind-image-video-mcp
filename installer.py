#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,platform,secrets,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;ENV=ROOT/".env"
def run(cmd):print("+"," ".join(map(str,cmd)));subprocess.run(cmd,check=True)
def main():
 a=argparse.ArgumentParser();a.add_argument("--repair",action="store_true");a.add_argument("--update",action="store_true");a.add_argument("--check",action="store_true");a.add_argument("--force",action="store_true");args=a.parse_args()
 print(f"Bina installer | {platform.system()} {platform.machine()}")
 if sys.version_info<(3,12):raise SystemExit("Python 3.12+ is required.")
 v=ROOT/".venv";py=v/("Scripts/python.exe" if os.name=="nt" else "bin/python")
 if args.check:print({"python":sys.version.split()[0],"venv":py.exists(),"env":ENV.exists(),"tailscale":bool(shutil.which("tailscale"))});return
 if args.force and v.exists():shutil.rmtree(v)
 if not py.exists():run([sys.executable,"-m","venv",str(v)])
 run([str(py),"-m","pip","install","--upgrade","pip"])
 run([str(py),"-m","pip","install","-e",str(ROOT)])
 if not ENV.exists():ENV.write_text(f"BINA_AUTH_TOKEN={secrets.token_urlsafe(32)}\nBINA_HOST=127.0.0.1\nBINA_PORT=8876\nBINA_PUBLIC_HOST=\nBINA_PUBLIC_PATH=/bina\nBINA_IMAGE_PROVIDER=mock\nBINA_VIDEO_PROVIDER=mock\n")
 if args.update:run([str(py),"-m","pip","install","--upgrade","-e",str(ROOT)])
 print("Installation complete.")
if __name__=="__main__":main()
