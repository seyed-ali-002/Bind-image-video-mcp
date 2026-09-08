from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import uuid
executor=ThreadPoolExecutor(max_workers=2); jobs={}
@dataclass
class Job: id:str; kind:str; status:str='queued'; result:str|None=None; error:str|None=None; created_at:str=''
def create(kind,fn):
 j=Job(uuid.uuid4().hex,kind,created_at=datetime.now(timezone.utc).isoformat()); jobs[j.id]=j
 def run():
  j.status='running'
  try: j.result=str(fn()); j.status='completed'
  except Exception as e: j.error=str(e); j.status='failed'
 executor.submit(run); return j
def get(job_id): return jobs.get(job_id)
def serialize(j): return asdict(j) if j else None
