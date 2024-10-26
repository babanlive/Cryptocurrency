from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn

from api.routers import router as api_router
from core.config import settings
from core.models import db_helper
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    router=api_router,
    prefix=settings.api.prefix,
)


if __name__ == '__main__':
    uvicorn.run('main:main_app', host=settings.run.host, port=settings.run.port, reload=True)
