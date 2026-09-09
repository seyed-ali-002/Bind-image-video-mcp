import secrets
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BINA_", env_file=".env", extra="ignore"
    )
    auth_token: str = ""
    host: str = "127.0.0.1"
    port: int = 8876
    public_host: str = ""
    public_scheme: str = "https"
    public_path: str = ""
    data_dir: Path = ROOT / "data"
    image_provider: str = "mock"
    video_provider: str = "mock"
    openai_api_key: str = ""
    openai_image_model: str = "gpt-image-1"
    replicate_api_token: str = ""
    replicate_image_model: str = "black-forest-labs/flux-schnell"
    replicate_video_model: str = "kwaivgi/kling-v1.6-standard"

    def ensure_token(self):
        if not self.auth_token:
            self.auth_token = secrets.token_urlsafe(32)
        return self.auth_token

    @property
    def connection_url(self):
        if not self.public_host:
            return f"http://{self.host}:{self.port}/mcp"
        path = self.public_path.strip("/")
        return (
            f"{self.public_scheme}://{self.public_host}/{path + '/' if path else ''}mcp"
        )


settings = Settings()
settings.ensure_token()
