from app.storage.manager import storage
from app.providers.registry import image_provider
from app.presets import apply
from app.db import record
def generate_image(prompt,width=1024,height=1024,preset=""):
 prompt=apply(prompt,preset);p=storage.path("image",".png");image_provider().generate(prompt,p,width,height);record("image",prompt,"active");return {"asset":p.name,"path":str(p),"prompt":prompt}
def edit_image(source,prompt):
 p=storage.images/source
 if not p.exists():raise FileNotFoundError(source)
 out=storage.path("image",".png");image_provider().edit(p,prompt,out);record("image_edit",prompt,"active");return {"asset":out.name,"path":str(out)}
def image_variation(source):return edit_image(source,"Create a variation of this image")
def upscale_image(source,scale=2):
 from PIL import Image
 if scale<2 or scale>8:raise ValueError("scale must be between 2 and 8")
 p=storage.images/source
 if not p.exists():raise FileNotFoundError(source)
 im=Image.open(p);out=storage.path("image",".png");im.resize((im.width*scale,im.height*scale)).save(out);return {"asset":out.name,"path":str(out)}
def remove_background(source):return edit_image(source,"Remove the background")
def analyze_image(source):
 from PIL import Image
 p=storage.images/source
 if not p.exists():raise FileNotFoundError(source)
 im=Image.open(p);return {"asset":source,"width":im.width,"height":im.height,"mode":im.mode,"format":im.format}
def compare_images(first,second):return {"first":analyze_image(first),"second":analyze_image(second)}
