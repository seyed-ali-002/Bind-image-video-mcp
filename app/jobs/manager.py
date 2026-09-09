from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import uuid,json
from app import db
executor=ThreadPoolExecutor(max_workers=4);jobs={};cancelled=set()
@dataclass
class Job:id:str;kind:str;status:str="queued";progress:int=0;result:object=None;error:str|None=None;created_at:str="";started_at:str|None=None;finished_at:str|None=None
def now():return datetime.now(timezone.utc).isoformat()
def create(kind,fn,metadata=None):
 j=Job(uuid.uuid4().hex,kind,created_at=now());jobs[j.id]=j;db.job_create(asdict(j)|{"metadata":metadata or {}})
 def run():
  if j.id in cancelled:return
  j.status="running";j.started_at=now();j.progress=5;db.job_update(j.id,status=j.status,progress=j.progress,started_at=j.started_at)
  try:
   def progress(value):j.progress=max(0,min(100,int(value)));db.job_update(j.id,progress=j.progress)
   result=fn(progress)
   if j.id in cancelled:j.status="cancelled";j.progress=0
   else:j.result=result;j.status="completed";j.progress=100
  except Exception as e:j.error=str(e);j.status="failed"
  j.finished_at=now();db.job_update(j.id,status=j.status,progress=j.progress,result=json.dumps(j.result,default=str) if j.result is not None else None,error=j.error,finished_at=j.finished_at)
 executor.submit(run);return j
def get(job_id):
 j=jobs.get(job_id)
 if j:return j
 d=db.job_get(job_id)
 if not d:return None
 try:d["result"]=json.loads(d["result"]) if d.get("result") else None
 except Exception:pass
 return d
def serialize(j):return None if not j else (asdict(j) if isinstance(j,Job) else j)
def list_jobs(limit=50,status=None):return db.jobs_list(limit,status)
def cancel(job_id):
 j=jobs.get(job_id)
 if j and j.status in ("queued","running"):cancelled.add(job_id);j.status="cancelled";db.job_update(job_id,status="cancelled");return True
 d=db.job_get(job_id)
 if d and d["status"] in ("queued","running"):db.job_update(job_id,status="cancelled");return True
 return False
def retry(job_id):return {"error":"retry requires resubmitting the original generation","job_id":job_id}
