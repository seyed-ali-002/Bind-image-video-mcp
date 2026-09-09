# Bina MCP Server

Cross-platform MCP server for image/video workflows with independent runtime from Dana.

## One-click
- Linux: `./install.sh`, then `./run.sh`
- macOS: `./install.command`, then `./run.command`
- Windows: `install.bat`, then `run.bat`

## Providers — Phase C
Bina uses a provider registry. Configure providers in `.env`:

```env
BINA_IMAGE_PROVIDER=mock
BINA_VIDEO_PROVIDER=mock

# OpenAI image generation
BINA_OPENAI_API_KEY=
BINA_OPENAI_IMAGE_MODEL=gpt-image-1

# Replicate image/video
BINA_REPLICATE_API_TOKEN=
BINA_REPLICATE_IMAGE_MODEL=black-forest-labs/flux-schnell
BINA_REPLICATE_VIDEO_MODEL=kwaivgi/kling-v1.6-standard
```

Supported:
- Image: `mock`, `openai`, `replicate`
- Video: `mock`, `replicate`

Check configuration:
`GET /providers` or MCP tool `bina_provider_status`.

## Runtime
`python runner.py start|stop|restart|status|doctor|connection`

Dana is never modified. Bina has independent data, runtime state, token, port and provider configuration.
