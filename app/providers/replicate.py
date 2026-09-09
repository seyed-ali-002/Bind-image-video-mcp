from .base import ImageProvider, VideoProvider
from .http import ProviderError, download, request_json


class _Replicate:
    def __init__(self, key, model):
        self.key = key
        self.model = model

    def headers(self):
        return {"Authorization": f"Bearer {self.key}", "Prefer": "wait"}

    def predict(self, input):
        if not self.key:
            raise ProviderError("REPLICATE_API_TOKEN is not configured")
        d = request_json(
            "https://api.replicate.com/v1/models/" + self.model + "/predictions",
            {"input": input},
            self.headers(),
            180,
        )
        out = d.get("output")
        if isinstance(out, list):
            out = out[0]
        if not out:
            raise ProviderError("Replicate returned no output")
        return out


class ReplicateImageProvider(_Replicate, ImageProvider):
    def generate(self, prompt, output, width=1024, height=1024):
        return download(
            self.predict({"prompt": prompt, "width": width, "height": height}), output
        )

    def edit(self, source, prompt, output):
        return self.generate(prompt, output)


class ReplicateVideoProvider(_Replicate, VideoProvider):
    def generate(self, prompt, output, duration=5):
        return download(self.predict({"prompt": prompt, "duration": duration}), output)

    def image_to_video(self, image, prompt, output, duration=5):
        return self.generate(prompt, output, duration)
