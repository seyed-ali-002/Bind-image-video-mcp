from pathlib import Path
import base64,urllib.request,json
from .base import ImageProvider
from .http import request_json,ProviderError
class OpenAIImageProvider(ImageProvider):
 def __init__(self,key,model="gpt-image-1"):self.key=key;self.model=model
 def _headers(self):return {"Authorization":f"Bearer {self.key}"}
 def generate(self,prompt,output,width=1024,height=1024):
  if not self.key:raise ProviderError("OPENAI_API_KEY is not configured")
  size=f"{width}x{height}" if width in (1024,1536) and height in (1024,1536) else "1024x1024"
  d=request_json("https://api.openai.com/v1/images/generations",{"model":self.model,"prompt":prompt,"size":size},self._headers())
  item=d["data"][0]
  if item.get("b64_json"):output.write_bytes(base64.b64decode(item["b64_json"]));return output
  raise ProviderError("OpenAI response did not include image bytes")
 def edit(self,source,prompt,output):
  raise ProviderError("OpenAI edit requires multipart transport; use generate or configure another editor provider")
