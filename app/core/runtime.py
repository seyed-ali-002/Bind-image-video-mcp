from __future__ import annotations
import json,os,signal,socket,time
from pathlib import Path
from app.core.config import settings
RUNTIME=Path(settings.data_dir)/"runtime";RUNTIME.mkdir(parents=True,exist_ok=True);PID=RUNTIME/"bina.json"
def is_port_free(port,host="127.0.0.1"):
 with socket.socket() as s:return s.connect_ex((host,port))!=0
def free_port(start):
 for port in range(start,start+100):
  if is_port_free(port):return port
 raise RuntimeError("No free port found in configured range")
def _read():
 try:return json.loads(PID.read_text())
 except (OSError,json.JSONDecodeError):return None
def running():
 data=_read()
 if not data:return None
 try:os.kill(int(data["pid"]),0);return data
 except (KeyError,OSError,TypeError,ValueError):PID.unlink(missing_ok=True);return None
def save(pid,port):PID.write_text(json.dumps({"pid":pid,"port":port,"started_at":time.time()}))
def clear():PID.unlink(missing_ok=True)
def stop(timeout=8):
 data=running()
 if not data:return {"status":"stopped","changed":False}
 try:os.kill(int(data["pid"]),signal.SIGTERM)
 except (ProcessLookupError,ValueError):clear();return {"status":"stopped","changed":False}
 end=time.time()+timeout
 while time.time()<end:
  if not running():return {"status":"stopped","changed":True}
  time.sleep(.2)
 try:os.kill(int(data["pid"]),signal.SIGKILL)
 except (ProcessLookupError,ValueError):pass
 clear();return {"status":"stopped","changed":True}
