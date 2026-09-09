import argparse,os
from app.core.config import settings
from app.core.doctor import doctor
from app.core.runtime import running
from app.db import history
def main():
 p=argparse.ArgumentParser(prog="bina"); s=p.add_subparsers(dest="cmd")
 s.add_parser("start");s.add_parser("connection");s.add_parser("token");s.add_parser("capabilities");s.add_parser("doctor");s.add_parser("status");h=s.add_parser("history");h.add_argument("--limit",type=int,default=50)
 a=p.parse_args()
 if a.cmd=="start": from app.main import main as run;run()
 elif a.cmd=="connection": print(settings.connection_url)
 elif a.cmd=="token": print(settings.auth_token)
 elif a.cmd=="capabilities": from app.mcp.server import bina_capabilities;print(bina_capabilities())
 elif a.cmd=="doctor": print(doctor())
 elif a.cmd=="status": print(running() or {"status":"stopped"})
 elif a.cmd=="history": print(history(a.limit))
 else:p.print_help()
