from .mock import MockImageProvider,MockVideoProvider
from .openai import OpenAIImageProvider
from .replicate import ReplicateImageProvider,ReplicateVideoProvider
from .http import ProviderError
from app.core.config import settings
def image_provider():
 p=settings.image_provider.lower()
 if p=="mock":return MockImageProvider()
 if p=="openai":return OpenAIImageProvider(settings.openai_api_key,settings.openai_image_model)
 if p=="replicate":return ReplicateImageProvider(settings.replicate_api_token,settings.replicate_image_model)
 raise ProviderError(f"Unsupported image provider: {p}. Supported: mock, openai, replicate")
def video_provider():
 p=settings.video_provider.lower()
 if p=="mock":return MockVideoProvider()
 if p=="replicate":return ReplicateVideoProvider(settings.replicate_api_token,settings.replicate_video_model)
 raise ProviderError(f"Unsupported video provider: {p}. Supported: mock, replicate")
def provider_status():
 def ok(name,key):return {"provider":name,"configured":bool(key)}
 return {"image":settings.image_provider,"video":settings.video_provider,"openai":ok("openai",settings.openai_api_key),"replicate":ok("replicate",settings.replicate_api_token)}
