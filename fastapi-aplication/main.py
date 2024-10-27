import asyncio

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn

from api.routers import router as api_router
from core.config import settings
from core.models import db_helper
from fastapi import FastAPI
from index_price import main as get_prices


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    task = asyncio.create_task(get_prices())
    try:
        yield
    finally:
        task.cancel()
        await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(
    router=api_router,
    prefix=settings.api.prefix,
)


if __name__ == '__main__':
    uvicorn.run('main:main_app', host=settings.run.host, port=settings.run.port, reload=True)
