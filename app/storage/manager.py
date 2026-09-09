import uuid
from pathlib import Path

from app.core.config import settings


class Storage:
    def __init__(self):
        self.root = Path(settings.data_dir)
        self.images = self.root / "images"
        self.videos = self.root / "videos"
        self.temp = self.root / "temp"
        for p in (self.images, self.videos, self.temp):
            p.mkdir(parents=True, exist_ok=True)

    def path(self, kind, suffix):
        return (
            self.images if kind == "image" else self.videos
        ) / f"{uuid.uuid4().hex}{suffix}"

    def list(self, kind):
        return [
            p.name
            for p in (self.images if kind == "image" else self.videos).iterdir()
            if p.is_file()
        ]

    def delete(self, kind, name):
        base = self.images if kind == "image" else self.videos
        p = (base / name).resolve()
        if base.resolve() not in p.parents:
            raise ValueError("Invalid asset path")
        if p.exists():
            p.unlink()
            return True
        return False


storage = Storage()
