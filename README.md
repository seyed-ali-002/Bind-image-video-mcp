# Bina MCP Server

Cross-platform MCP server for image/video generation, editing and media processing.

## One-click
- Linux: `./install.sh`, then `./run.sh`
- macOS: `./install.command`, then `./run.command`
- Windows: `install.bat`, then `run.bat`

## Phase D — Media Pipeline
Bina now has a real FFmpeg-based media pipeline:

- Video metadata probe
- MP4 transcoding
- Video trim
- Thumbnail extraction
- Video concatenation
- Persistent asynchronous jobs
- Progress and asset registration

Requirements for media operations:

```bash
sudo apt install ffmpeg
```

MCP tools:
`media_probe`, `transcode_video`, `trim_video`, `thumbnail_video`, `concat_videos`.

HTTP:
- `GET /media/ffmpeg`
- `GET /media/probe/{source}`
- `POST /media/transcode/{source}`
- `POST /media/trim/{source}`
- `POST /media/thumbnail/{source}`
- `POST /media/concat`

## Providers
Image: `mock`, `openai`, `replicate`
Video: `mock`, `replicate`

Dana is never modified. Bina has independent runtime, token, storage, jobs and media processing.
