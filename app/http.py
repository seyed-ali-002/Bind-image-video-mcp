from fastapi import FastAPI,Header,HTTPException
from app.core.config import settings
from app.core.security import authorize
from app.mcp.server import mcp
app=FastAPI(title='Bina MCP Server',version='0.1.0')
@app.get('/health')
def health(): return {'status':'ok','service':'bina'}
@app.get('/connection')
def connection(authorization:str|None=Header(default=None)):
 authorize(authorization); return {'url':settings.connection_url,'token':settings.auth_token}
app.mount('/mcp',mcp.streamable_http_app())
