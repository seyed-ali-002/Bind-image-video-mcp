from app.storage.manager import storage
from app.providers.registry import video_provider
from app.jobs.manager import create,get,serialize,list_jobs,cancel,retry
from app.assets import register
from app import db
def _job(kind,prompt,work):
 def run(progress):
  progress(20);p=work();progress(90);aid=register("video",p,prompt,"active",metadata={"operation":kind});db.record(kind,prompt,"active","completed",aid);progress(100);return {"asset_id":aid,"asset":p.name,"path":str(p)}
 return create(kind,run,{"prompt":prompt}).id
def generate_video(prompt,duration=5):
 return _job("generate_video",prompt,lambda: _generate(prompt,duration))
def _generate(prompt,duration):p=storage.path("video",".mp4");video_provider().generate(prompt,p,duration);return p
def image_to_video(image,prompt="",duration=5):
 src=storage.images/image
 if not src.exists():raise FileNotFoundError(image)
 return _job("image_to_video",prompt,lambda:_i2v(src,prompt,duration))
def _i2v(src,prompt,duration):p=storage.path("video",".mp4");video_provider().image_to_video(src,prompt,p,duration);return p
def get_generation_status(job_id):return serialize(get(job_id)) or {"error":"job_not_found"}
def get_generation_result(job_id):return get_generation_status(job_id)
def list_generation_jobs(limit=50,status=None):return list_jobs(limit,status)
def cancel_generation(job_id):return {"cancelled":cancel(job_id),"job_id":job_id}
def retry_generation(job_id):return retry(job_id)
def edit_video(source,prompt):
 src=storage.videos/source
 if not src.exists():raise FileNotFoundError(source)
 return _job("edit_video",prompt,lambda:_edit(src,prompt))
def _edit(src,prompt):p=storage.path("video",".mp4");p.write_bytes(src.read_bytes()+f"\nEDIT:{prompt}".encode());return p
def extend_video(source,duration=5):return edit_video(source,f"Extend by {duration} seconds")
