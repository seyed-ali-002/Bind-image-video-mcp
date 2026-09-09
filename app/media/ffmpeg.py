from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def available():
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def _run(cmd):
    if not available():
        raise RuntimeError("FFmpeg and FFprobe are required")
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def run(args):
    return _run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *map(str, args)]
    ).stdout


def probe(path):
    r = _run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate",
            "-of",
            "json",
            str(path),
        ]
    )
    return json.loads(r.stdout)


def transcode(source, output, codec="libx264", crf=23):
    run(["-i", source, "-c:v", codec, "-crf", str(crf), "-c:a", "aac", output])
    return Path(output)


def trim(source, output, start=0, end=None):
    args = ["-ss", str(start), "-i", source]
    if end is not None:
        args += ["-t", str(max(0.01, float(end) - float(start)))]
    args += ["-c", "copy", output]
    run(args)
    return Path(output)


def thumbnail(source, output, time=0):
    run(["-ss", str(time), "-i", source, "-frames:v", "1", output])
    return Path(output)


def concat(sources, output):
    listfile = Path(output).with_suffix(".concat.txt")
    listfile.write_text("".join(f"file '{Path(x).resolve()}'\n" for x in sources))
    try:
        run(["-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", output])
    finally:
        listfile.unlink(missing_ok=True)
    return Path(output)
