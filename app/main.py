import os

import uvicorn

from app.core.banner import startup
from app.core.config import settings
from app.core.runtime import clear, free_port, save


def main():
    port = free_port(int(os.getenv("BINA_PORT", settings.port)))
    settings.port = port
    save(os.getpid(), port)
    startup(port)
    try:
        uvicorn.run(
            "app.http:app",
            host=settings.host,
            port=port,
            workers=1,
            log_level="warning",
        )
    finally:
        clear()


if __name__ == "__main__":
    main()
