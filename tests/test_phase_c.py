from app.providers.http import ProviderError
from app.providers.registry import image_provider, provider_status, video_provider


def test_mock_providers():
    assert (
        image_provider().__class__.__name__ == "MockImageProvider"
        and video_provider().__class__.__name__ == "MockVideoProvider"
    )


def test_provider_status():
    d = provider_status()
    assert "openai" in d and "replicate" in d


def test_unknown_provider(monkeypatch):
    import app.providers.registry as r

    monkeypatch.setattr(r.settings, "image_provider", "unknown")
    try:
        r.image_provider()
        assert False
    except ProviderError:
        assert True
