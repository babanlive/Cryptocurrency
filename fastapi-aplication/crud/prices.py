from collections.abc import Sequence
from datetime import datetime

from core.models import Price
from core.schemas.prices import PriceCreate
from fastapi import HTTPException
from sqlalchemy import Date, cast, select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_prices(session: AsyncSession, ticker: str) -> Sequence[Price]:
    await ticker_exists(session, ticker)
    stmt = select(Price).where(Price.ticker == ticker)
    result = await session.scalars(stmt)
    return result.all()


async def get_price_by_date(session: AsyncSession, ticker: str, date: datetime) -> Sequence[Price]:
    await ticker_exists(session, ticker)
    stmt = select(Price).where(Price.ticker == ticker, cast(Price.timestamp, Date) == date.date())
    result = await session.scalars(stmt)
    return result.all()


async def get_latest_price(session: AsyncSession, ticker: str) -> Price | None:
    await ticker_exists(session, ticker)
    stmt = select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc())
    result = await session.scalars(stmt)
    return result.first()


async def add_price(session: AsyncSession, price_data: PriceCreate) -> None:
    new_price = Price(
        ticker=price_data.ticker,
        price=price_data.price,
        timestamp=price_data.timestamp,
    )
    session.add(new_price)
    await session.commit()


async def ticker_exists(session: AsyncSession, ticker: str) -> None:
    stmt = select(Price).where(Price.ticker == ticker).limit(1)
    result = await session.scalar(stmt)
    if result is None:
        raise HTTPException(status_code=404, detail='Ticker not found')
