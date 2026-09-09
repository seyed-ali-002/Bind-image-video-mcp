from __future__ import annotations
import sqlite3,json
from pathlib import Path
from app.core.config import settings
DB=Path(settings.data_dir)/"bina.db"; DB.parent.mkdir(parents=True,exist_ok=True)
def conn():
 c=sqlite3.connect(DB,check_same_thread=False);c.row_factory=sqlite3.Row
 c.executescript("""create table if not exists history(id integer primary key autoincrement,kind text,prompt text,provider text,status text,asset_id text,metadata text default '{}',created_at text default current_timestamp);
 create table if not exists jobs(id text primary key,kind text,status text,progress integer default 0,result text,error text,created_at text,started_at text,finished_at text,metadata text default '{}');
 create table if not exists assets(id text primary key,kind text,name text,path text unique,prompt text,provider text,job_id text,metadata text default '{}',created_at text default current_timestamp);""")
 cols={r[1] for r in c.execute("pragma table_info(history)")}
 if "asset_id" not in cols:c.execute("alter table history add column asset_id text")
 if "metadata" not in cols:c.execute("alter table history add column metadata text default '{}' ")
 c.commit();return c
def _rows(q,args=()):
 c=conn();r=[dict(x) for x in c.execute(q,args)];c.close();return r
def record(kind,prompt,provider,status="completed",asset_id=None,metadata=None):
 c=conn();c.execute("insert into history(kind,prompt,provider,status,asset_id,metadata) values(?,?,?,?,?,?)",(kind,prompt,provider,status,asset_id,json.dumps(metadata or {})));c.commit();c.close()
def history(limit=50,status=None):
 q="select * from history";a=[]
 if status:q+=" where status=?";a.append(status)
 q+=" order by id desc limit ?";a.append(limit);return _rows(q,a)
def job_create(d):
 c=conn();c.execute("insert into jobs(id,kind,status,progress,created_at,metadata) values(?,?,?,?,?,?)",(d["id"],d["kind"],"queued",0,d["created_at"],json.dumps(d.get("metadata",{}))));c.commit();c.close()
def job_update(job_id,**kw):
 allowed={"status","progress","result","error","started_at","finished_at","metadata"};vals=[];sets=[]
 for k,v in kw.items():
  if k in allowed:sets.append(k+"=?");vals.append(json.dumps(v) if k=="metadata" else v)
 if sets:
  vals.append(job_id);c=conn();c.execute("update jobs set "+",".join(sets)+" where id=?",vals);c.commit();c.close()
def job_get(job_id):
 r=_rows("select * from jobs where id=?",(job_id,));return r[0] if r else None
def jobs_list(limit=50,status=None):
 q="select * from jobs";a=[]
 if status:q+=" where status=?";a.append(status)
 q+=" order by created_at desc limit ?";a.append(limit);return _rows(q,a)
def asset_add(**d):
 c=conn();c.execute("insert into assets(id,kind,name,path,prompt,provider,job_id,metadata) values(?,?,?,?,?,?,?,?)",(d["id"],d["kind"],d["name"],d["path"],d.get("prompt",""),d.get("provider",""),d.get("job_id"),json.dumps(d.get("metadata",{}))));c.commit();c.close()
def assets_list(kind=None,limit=100):
 q="select * from assets";a=[]
 if kind:q+=" where kind=?";a.append(kind)
 q+=" order by created_at desc limit ?";a.append(limit);return _rows(q,a)
def asset_get(asset_id):
 r=_rows("select * from assets where id=? or name=?",(asset_id,asset_id));return r[0] if r else None
def asset_delete(asset_id):
 c=conn();c.execute("delete from assets where id=? or name=?",(asset_id,asset_id));n=c.total_changes;c.commit();c.close();return bool(n)
