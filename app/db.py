from __future__ import annotations
import sqlite3,json
from pathlib import Path
from app.core.config import settings
DB=Path(settings.data_dir)/"bina.db"; DB.parent.mkdir(parents=True,exist_ok=True)
def conn():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
 c.execute("create table if not exists history(id integer primary key, kind text,prompt text,provider text,status text,created_at text default current_timestamp)")
 return c
def record(kind,prompt,provider,status="completed"):
 c=conn(); c.execute("insert into history(kind,prompt,provider,status) values(?,?,?,?)",(kind,prompt,provider,status));c.commit();c.close()
def history(limit=50):
 c=conn();r=[dict(x) for x in c.execute("select * from history order by id desc limit ?",(limit,))];c.close();return r
