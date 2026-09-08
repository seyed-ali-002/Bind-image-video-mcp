from app.storage.manager import storage
from app.providers.registry import video_provider
from app.jobs.manager import create

def generate_video(prompt,duration=5):
 def work():
  p=storage.path('video','.mp4'); video_provider().generate(prompt,p,duration); return p
 return create('generate_video',work).id

def image_to_video(image,prompt='',duration=5):
 src=storage.images/image
 if not src.exists(): raise FileNotFoundError(image)
 def work():
  p=storage.path('video','.mp4'); video_provider().image_to_video(src,prompt,p,duration); return p
 return create('image_to_video',work).id

def get_generation_status(job_id):
 from app.jobs.manager import get,serialize
 j=get(job_id)
 return serialize(j) if j else {'error':'job_not_found'}

def get_generation_result(job_id): return get_generation_status(job_id)

def edit_video(source,prompt):
 src=storage.videos/source
 if not src.exists(): raise FileNotFoundError(source)
 def work():
  p=storage.path('video','.mp4'); p.write_bytes(src.read_bytes()+f'\nEDIT:{prompt}'.encode()); return p
 return create('edit_video',work).id

def extend_video(source,duration=5): return edit_video(source,f'Extend by {duration} seconds')
