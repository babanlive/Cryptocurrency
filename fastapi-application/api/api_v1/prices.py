from datetime import datetime

from core.models import db_helper
from core.schemas.prices import PriceRead
from crud import prices as crud_prices
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=['Prices'])


@router.get('/tickers', response_model=list[PriceRead])
async def get_tickers(ticker: str = Query(...), session: AsyncSession = Depends(db_helper.session_getter)):  # noqa: B008
    return await crud_prices.get_prices(session, ticker)


@router.get('/tickers/date', response_model=list[PriceRead])
async def get_price_by_date(
    ticker: str = Query(...),
    date: datetime = Query(...),  # noqa: B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa: B008
):
    return await crud_prices.get_price_by_date(session, ticker, date)


@router.get('/tickers/latest', response_model=PriceRead)
async def get_latest_price(ticker: str = Query(...), session: AsyncSession = Depends(db_helper.session_getter)):  # noqa: B008
    return await crud_prices.get_latest_price(session, ticker)
