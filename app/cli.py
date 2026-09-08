import argparse,subprocess,sys
from app.core.config import settings
def main():
 p=argparse.ArgumentParser(prog='bina'); sub=p.add_subparsers(dest='cmd'); sub.add_parser('start'); sub.add_parser('connection'); sub.add_parser('token'); sub.add_parser('capabilities'); a=sub.parse_args()
 if a.cmd=='start': from app.main import main as run; run()
 elif a.cmd=='connection': print(settings.connection_url)
 elif a.cmd=='token': print(settings.auth_token)
 elif a.cmd=='capabilities': from app.mcp.server import bina_capabilities; print(bina_capabilities())
 else: p.print_help()
