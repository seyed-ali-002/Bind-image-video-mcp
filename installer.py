#!/usr/bin/env python3
from __future__ import annotations
import os, platform, secrets, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = ROOT / '.env'

def run(cmd, **kw):
    print('+', ' '.join(map(str, cmd)))
    subprocess.run(cmd, check=True, **kw)

def main():
    print(f'Bina installer | {platform.system()} {platform.machine()}')
    if sys.version_info < (3, 12): raise SystemExit('Python 3.12+ is required.')
    venv = ROOT / '.venv'
    py = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not py.exists(): run([sys.executable, '-m', 'venv', str(venv)])
    run([str(py), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([str(py), '-m', 'pip', 'install', '-e', str(ROOT)])
    if not ENV.exists():
        token = secrets.token_urlsafe(32)
        ENV.write_text(f'BINA_AUTH_TOKEN={token}\nBINA_HOST=127.0.0.1\nBINA_PORT=8876\nBINA_PUBLIC_HOST=\nBINA_PUBLIC_PATH=/bina\nBINA_IMAGE_PROVIDER=mock\nBINA_VIDEO_PROVIDER=mock\n', encoding='utf-8')
    print('\nInstallation complete. Run the platform launcher or runner.')

if __name__ == '__main__': main()
