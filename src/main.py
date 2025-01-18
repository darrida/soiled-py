import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

if True:
    from _core.asgi import application
from _core import settings

logger.remove()
logger.add(sys.stderr)

app = FastAPI(docs_url=None, redoc_url=None)


logger.info("Mounting static assets path...")
app.mount("/static", StaticFiles(directory=settings.STATIC_ROOT, check_dir=True), name="assets")
# logger.info("Mounting media storage path...")
# app.mount("/apps/storage", StaticFiles(directory=settings.MEDIA_ROOT, check_dir=True), name="storage")

# logger.info("Mounting legacy flask webapps redirect routes...")
# app.mount("/webapps", flast_webapps_app, "Legacy Flask App Redirects")

logger.info("Mounting django/django-ninja application...")
app.mount("", application, "Django")


async def main():
    config = uvicorn.Config(
        app="main:app",
        host=os.environ.get("HOST", "0.0.0.0"),  # noqa: S104
        port=int(os.environ.get("PORT", 6010)),
        log_level=os.environ.get("LOG_LEVEL", "info"),
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())