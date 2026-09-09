#!/usr/bin/env python3
from __future__ import annotations
import argparse,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent;PY=ROOT/".venv"/("Scripts/python.exe" if os.name=="nt" else "bin/python")
def main():
 parser=argparse.ArgumentParser();parser.add_argument("command",nargs="?",default="start",choices=["start","stop","restart","status","doctor","connection"]);args=parser.parse_args()
 if not PY.exists():subprocess.run([sys.executable,str(ROOT/"installer.py")],check=True)
 os.chdir(ROOT);cmd=[str(PY),"-m","app.cli",args.command]
 if args.command=="start":
  result=subprocess.run([str(PY),"-m","app.cli","status"],capture_output=True,text=True,check=False)
  if '"pid"' in result.stdout:print("Bina is already running:",result.stdout);return
  subprocess.run([str(PY),"-m","app.cli","doctor"],check=False);os.execv(str(PY),[str(PY),"-m","app.main"])
 subprocess.run(cmd,check=False)
if __name__=="__main__":main()
