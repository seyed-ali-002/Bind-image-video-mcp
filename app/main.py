import uvicorn
from app.core.config import settings
from app.http import app
def main(): uvicorn.run(app,host=settings.host,port=settings.port,workers=1)
if __name__=='__main__': main()
