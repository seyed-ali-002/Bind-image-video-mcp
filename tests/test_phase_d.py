from pathlib import Path
from app.media.ffmpeg import available
from app.media.tools import concat_videos
def test_ffmpeg_status_type():assert isinstance(available(),bool)
def test_concat_requires_two():
 try:concat_videos([]);assert False
 except ValueError:assert True
