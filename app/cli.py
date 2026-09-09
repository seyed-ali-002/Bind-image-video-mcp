import argparse,secrets,subprocess,sys
from pathlib import Path
from app.core.config import settings
from app.core.doctor import doctor
from app.core.runtime import running,stop
from app.core.connection import info
from app.db import history
ROOT=Path(__file__).resolve().parents[1]
def rotate():
 token=secrets.token_urlsafe(32);p=ROOT/".env";lines=p.read_text().splitlines() if p.exists() else []
 lines=[f"BINA_AUTH_TOKEN={token}" if x.startswith("BINA_AUTH_TOKEN=") else x for x in lines]
 if not any(x.startswith("BINA_AUTH_TOKEN=") for x in lines):lines.append(f"BINA_AUTH_TOKEN={token}")
 p.write_text("\n".join(lines)+"\n");settings.auth_token=token;return token
def main():
 p=argparse.ArgumentParser(prog="bina");s=p.add_subparsers(dest="cmd")
 for x in ("start","stop","restart","connection","capabilities","doctor","status","token","rotate-token"):s.add_parser(x)
 h=s.add_parser("history");h.add_argument("--limit",type=int,default=50);a=p.parse_args()
 if a.cmd=="start":from app.main import main as run;run()
 elif a.cmd=="stop":print(stop())
 elif a.cmd=="restart":stop();subprocess.Popen([sys.executable,"-m","app.main"],cwd=ROOT)
 elif a.cmd=="connection":print(info(mask_token=False))
 elif a.cmd=="token":print(settings.auth_token)
 elif a.cmd=="rotate-token":print(rotate())
 elif a.cmd=="capabilities":from app.mcp.server import bina_capabilities;print(bina_capabilities())
 elif a.cmd=="doctor":print(doctor())
 elif a.cmd=="status":print(running() or {"status":"stopped"})
 elif a.cmd=="history":print(history(a.limit))
 else:p.print_help()
