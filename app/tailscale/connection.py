import json,subprocess
from app.core.config import settings
def tailscale_available():
 try: subprocess.run(['tailscale','version'],check=True,capture_output=True); return True
 except (FileNotFoundError,subprocess.CalledProcessError): return False
def status():
 if not tailscale_available(): return {'available':False}
 r=subprocess.run(['tailscale','status','--json'],capture_output=True,text=True,check=False)
 try: return {'available':True,'status':json.loads(r.stdout)}
 except json.JSONDecodeError: return {'available':True,'raw':r.stdout,'error':r.stderr}
def connection_url(host): return f'https://{host}/{settings.auth_token}/mcp'
