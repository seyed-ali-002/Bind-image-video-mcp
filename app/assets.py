from pathlib import Path
import uuid
from app.storage.manager import storage
from app import db
def register(kind,path,prompt="",provider="",job_id=None,metadata=None):
 p=Path(path);aid=uuid.uuid4().hex;db.asset_add(id=aid,kind=kind,name=p.name,path=str(p),prompt=prompt,provider=provider,job_id=job_id,metadata=metadata or {});return aid
def stats():return {"images":len(storage.list("image")),"videos":len(storage.list("video")),"root":str(storage.root),"registered_assets":len(db.assets_list(limit=100000))}
def list_assets(kind=None,limit=100):return db.assets_list(kind,limit)
def get_asset(asset_id):return db.asset_get(asset_id)
def delete_asset(kind,asset):
 d=db.asset_get(asset);name=d["name"] if d else asset;ok=storage.delete(kind,name);db.asset_delete(asset);return ok
