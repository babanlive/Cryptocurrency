from collections.abc import Sequence
from datetime import datetime

from core.models import Price
from core.schemas.prices import PriceCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_prices(session: AsyncSession, ticker: str) -> Sequence[Price]:
    stmt = select(Price).where(Price.ticker == ticker)
    result = await session.scalars(stmt)
    return result.all()


async def get_price_by_date(session: AsyncSession, ticker: str, date: datetime) -> Sequence[Price]:
    stmt = select(Price).where(Price.ticker == ticker, Price.timestamp >= date)
    result = await session.scalars(stmt)
    return result.all()


async def get_latest_price(session: AsyncSession, ticker: str) -> Price | None:
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
