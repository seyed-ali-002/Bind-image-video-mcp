from pathlib import Path
from PIL import Image,ImageDraw
from .base import ImageProvider,VideoProvider
class MockImageProvider(ImageProvider):
 def generate(self,prompt,output,width=1024,height=1024):
  im=Image.new('RGB',(width,height),(32,40,55)); ImageDraw.Draw(im).text((30,30),'Bina Mock\n'+prompt[:500],fill='white'); im.save(output); return output
 def edit(self,source,prompt,output):
  im=Image.open(source).convert('RGB'); ImageDraw.Draw(im).text((20,20),'Bina Edit: '+prompt[:300],fill='white'); im.save(output); return output
class MockVideoProvider(VideoProvider):
 def generate(self,prompt,output,duration=5): output.write_text(f'BINA-MOCK-VIDEO\nduration={duration}\nprompt={prompt}\n'); return output
 def image_to_video(self,image,prompt,output,duration=5): return self.generate(prompt,output,duration)
