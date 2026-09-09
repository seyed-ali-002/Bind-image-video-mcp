import os

import uvicorn

from app.core.config import settings
from app.core.runtime import clear, free_port, save
from app.http import app


def main():
    port = free_port(int(os.getenv("BINA_PORT", settings.port)))
    settings.port = port
    save(os.getpid(), port)
    print(f"Bina local: http://{settings.host}:{port}")
    print(f"Bina MCP: http://{settings.host}:{port}/mcp")
    try:
        uvicorn.run(app, host=settings.host, port=port, workers=1)
    finally:
        clear()


if __name__ == "__main__":
    main()
