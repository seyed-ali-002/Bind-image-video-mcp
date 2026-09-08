from .mock import MockImageProvider,MockVideoProvider
from app.core.config import settings
def image_provider():
 if settings.image_provider=='mock': return MockImageProvider()
 raise RuntimeError(f'Unsupported image provider: {settings.image_provider}')
def video_provider():
 if settings.video_provider=='mock': return MockVideoProvider()
 raise RuntimeError(f'Unsupported video provider: {settings.video_provider}')
