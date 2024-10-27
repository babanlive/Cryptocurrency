from core.config import settings
from fastapi import APIRouter

from .prices import router as prices_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(
    router=prices_router,
    prefix=settings.api.v1.prices,
)
