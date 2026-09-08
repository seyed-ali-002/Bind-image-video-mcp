# Bina MCP Server

Independent MCP server for image/video generation and editing. It uses Streamable HTTP, its own port/token/data directory and provider configuration. Dana is not modified.

## Run
`python -m venv .venv && . .venv/bin/activate && pip install -e . && cp .env.example .env && python -m app.main`

Endpoints: `/health`, authenticated `/connection`, MCP `/mcp`.

Tools: `bina_capabilities`, `generate_image`, `edit_image`, `image_variation`, `upscale_image`, `remove_background`, `generate_video`, `image_to_video`, `get_generation_status`, `get_generation_result`, `edit_video`, `extend_video`, `list_assets`, `delete_asset`.

Video generation is asynchronous and returns a job id. Mock providers provide deterministic end-to-end testing without paid API credentials. Production providers implement `app/providers/base.py` and are selected by environment configuration.

Tailscale detection is isolated in `app/tailscale/connection.py`; Bina does not claim Dana's existing Funnel route. Use an independent Tailscale identity or a shared reverse proxy with a unique Bina path.
