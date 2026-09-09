from __future__ import annotations
import json, socket, os
from pathlib import Path
from app.core.config import settings
RUNTIME=Path(settings.data_dir)/"runtime"; RUNTIME.mkdir(parents=True,exist_ok=True)
PID=RUNTIME/"bina.json"
def free_port(start:int):
 p=start
 while p<start+100:
  with socket.socket() as s:
   if s.connect_ex(("127.0.0.1",p))!=0:return p
  p+=1
 raise RuntimeError("No free port found")
def running():
 try:
  d=json.loads(PID.read_text()); os.kill(d["pid"],0); return d
 except Exception:return None
def save(pid,port): PID.write_text(json.dumps({"pid":pid,"port":port}))
def clear(): PID.unlink(missing_ok=True)
