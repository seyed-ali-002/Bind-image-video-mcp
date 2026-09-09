from app.media.ffmpeg import available,probe,transcode,trim,thumbnail,concat
from app.storage.manager import storage
from app.jobs.manager import create
from app.assets import register
from app import db
def _video(name):
 p=storage.videos/name
 if not p.exists():raise FileNotFoundError(name)
 return p
def _submit(kind,prompt,fn):
 def work(progress):
  progress(15);p=fn();progress(85);aid=register("video",p,prompt,"ffmpeg",metadata={"operation":kind});db.record(kind,prompt,"ffmpeg","completed",aid,{"operation":kind});progress(100);return {"asset_id":aid,"asset":p.name,"path":str(p)}
 return create(kind,work,{"prompt":prompt,"engine":"ffmpeg"}).id
def media_probe(source):return probe(_video(source))
def transcode_video(source,crf=23):
 src=_video(source);out=storage.path("video",".mp4");return _submit("transcode_video",source,lambda:transcode(src,out,crf=crf))
def trim_video(source,start=0,end=None):
 src=_video(source);out=storage.path("video",".mp4");return _submit("trim_video",source,lambda:trim(src,out,start,end))
def thumbnail_video(source,time=0):
 src=_video(source);out=storage.path("image",".jpg")
 def work(progress):
  progress(20);thumbnail(src,out,time);aid=register("image",out,source,"ffmpeg",metadata={"operation":"thumbnail","time":time});db.record("thumbnail",source,"ffmpeg","completed",aid);progress(100);return {"asset_id":aid,"asset":out.name,"path":str(out)}
 return create("thumbnail_video",work,{"source":source}).id
def concat_videos(sources):
 if len(sources)<2:raise ValueError("At least two videos are required")
 src=[_video(x) for x in sources];out=storage.path("video",".mp4");return _submit("concat_videos","concat",lambda:concat(src,out))
def ffmpeg_status():return {"available":available()}
