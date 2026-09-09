from __future__ import annotations

import platform
import shutil


def info():
    return {
        "os": platform.system().lower(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "tailscale": bool(shutil.which("tailscale")),
    }


def python_executable(venv):
    from pathlib import Path

    p = Path(venv)
    return p / (
        "Scripts/python.exe" if platform.system().lower() == "windows" else "bin/python"
    )
