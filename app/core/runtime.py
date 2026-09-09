from __future__ import annotations
import json,os,socket,signal,time
from pathlib import Path
from app.core.config import settings
RUNTIME=Path(settings.data_dir)/"runtime";RUNTIME.mkdir(parents=True,exist_ok=True);PID=RUNTIME/"bina.json"
def is_port_free(port,host="127.0.0.1"):
 with socket.socket() as s:return s.connect_ex((host,port))!=0
def free_port(start:int):
 for p in range(start,start+100):
  if is_port_free(p):return p
 raise RuntimeError("No free port found in configured range")
def _read():
 try:return json.loads(PID.read_text())
 except Exception:return None
def running():
 d=_read()
 if not d:return None
 try:os.kill(int(d["pid"]),0);return d
 except (OSError,ValueError):PID.unlink(missing_ok=True);return None
def save(pid,port):PID.write_text(json.dumps({"pid":pid,"port":port,"started_at":time.time()}))
def clear():PID.unlink(missing_ok=True)
def stop(timeout=8):
 d=running()
 if not d:return {"status":"stopped","changed":False}
 try:os.kill(int(d["pid"]),signal.SIGTERM)
 except ProcessLookupError:clear();return {"status":"stopped","changed":False}
 end=time.time()+timeout
 while time.time()<end:
  if not running():return {"status":"stopped","changed":True}
  time.sleep(.2)
 try:os.kill(int(d["pid"]),signal.SIGKILL)
 except ProcessLookupError:pass
 clear();return {"status":"stopped","changed":True}
