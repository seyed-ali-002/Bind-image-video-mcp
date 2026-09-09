import time
from app import db
from app.jobs.manager import create,get,serialize,cancel
from app.assets import register,list_assets,get_asset
from app.storage.manager import storage
def wait(j):
 for _ in range(50):
  s=serialize(get(j))
  if s["status"] in ("completed","failed","cancelled"):return s
  time.sleep(.02)
def test_persistent_job_progress():
 jid=create("test",lambda progress:(progress(40),{"ok":True})[1]).id;s=wait(jid);assert s["status"]=="completed" and s["progress"]==100;assert db.job_get(jid)
def test_asset_metadata():
 p=storage.path("image",".txt");p.write_text("x");aid=register("image",p,"p","mock");assert get_asset(aid)["id"]==aid and list_assets("image")
def test_cancel_unknown():assert cancel("missing") is False
def test_history_metadata():db.record("test","prompt","mock","completed",metadata={"x":1});assert db.history(1)
