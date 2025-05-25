import asyncio
import os
import sys

import uvicorn
from loguru import logger
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles

if True:
    from _core.asgi import django_asgi_app
from _core import settings

logger.remove()
logger.add(sys.stderr)

app = Starlette()


logger.info("Mounting static assets path...")
app.mount("/static", StaticFiles(directory=settings.STATIC_ROOT, check_dir=True), name="assets")

logger.info("Mounting django/django-ninja application...")
app.mount("", django_asgi_app, "Django")


async def main():
    config = uvicorn.Config(
        app="main:app",
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 8000)),
        log_level=os.environ.get("LOG_LEVEL", "info"),
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())