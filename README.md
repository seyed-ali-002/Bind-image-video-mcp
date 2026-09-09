# Bina MCP Server

Cross-platform MCP server for image/video generation, editing, processing and asset delivery.

## One-click
- Linux: `./install.sh`, then `./run.sh`
- macOS: `./install.command`, then `./run.command`
- Windows: `install.bat`, then `run.bat`

## Phase E — Asset Delivery & Lifecycle
Bina now provides a complete asset delivery layer:

- Persistent asset metadata
- Safe filesystem resolution
- Asset manifest with MIME type and file size
- Inline preview for images/videos
- Download endpoint
- Search by name, prompt and provider
- ZIP export with JSON manifest
- Missing-file detection
- Path traversal protection

HTTP:
- `GET /assets?kind=image&query=...`
- `GET /assets/{asset_id}`
- `GET /assets/{asset_id}/preview`
- `GET /assets/{asset_id}/download`
- `POST /assets/export`
- `DELETE /assets/{kind}/{asset_id}`

MCP:
- `bina_list_assets`
- `bina_get_asset`
- `bina_export_assets`

## Providers
Image: `mock`, `openai`, `replicate`
Video: `mock`, `replicate`

Dana is never modified. Bina has independent runtime, token, storage, jobs and media processing.
