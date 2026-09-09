#!/usr/bin/env python3
from __future__ import annotations
import os,platform,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
py=ROOT/".venv"/("Scripts/python.exe" if os.name=="nt" else "bin/python")
def main():
 if not py.exists(): subprocess.run([sys.executable,str(ROOT/"installer.py")],check=True)
 os.chdir(ROOT); print(f"Starting Bina on {platform.system()}...")
 subprocess.run([str(py),"-m","app.cli","doctor"],check=False)
 os.execv(str(py),[str(py),"-m","app.main"])
if __name__=="__main__":main()
