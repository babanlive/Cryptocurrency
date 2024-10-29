from core.models import Price
from core.schemas.prices import PriceCreate
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import Date, cast, select
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_price(ac: AsyncClient, add_price_data: list[PriceCreate], async_session_fixture) -> None:
    async with async_session_fixture as session:
        ticker = add_price_data[0].ticker
        response = await ac.get(f'/api/v1/prices/tickers?ticker={ticker}')

        stmt = select(Price).where(
            Price.ticker == ticker, cast(Price.timestamp, Date) == add_price_data[0].timestamp.date()
        )
        result = await session.execute(stmt)
        result_all = result.scalars().all()

        assert response.status_code == status.HTTP_200_OK
        assert result_all[0].price == add_price_data[0].price


async def test_get_latest_price(ac: AsyncClient, add_price_data: list[PriceCreate], async_session_fixture) -> None:
    async with async_session_fixture as session:
        ticker = add_price_data[0].ticker
        response = await ac.get(f'/api/v1/prices/tickers/latest?ticker={ticker}')
        latest_price = max((price for price in add_price_data if price.ticker == ticker), key=lambda x: x.timestamp)

        stmt = select(Price).where(Price.ticker == ticker).order_by(Price.timestamp.desc())
        result = await session.scalars(stmt)
        last_result = result.first()

        assert response.status_code == status.HTTP_200_OK
        assert last_result.price == latest_price.price


async def test_get_price_by_date(
    ac: AsyncClient, add_price_data: list[PriceCreate], async_session_fixture: AsyncSession
) -> None:
    async with async_session_fixture as session:
        ticker = add_price_data[0].ticker
        response = await ac.get(
            f'/api/v1/prices/tickers/date?ticker={ticker}&date={add_price_data[0].timestamp.date()}'
        )

        stmt = select(Price).where(
            Price.ticker == ticker, cast(Price.timestamp, Date) == add_price_data[0].timestamp.date()
        )
        result = await session.execute(stmt)
        all_result = result.scalars().all()

        assert response.status_code == status.HTTP_200_OK
        assert any(result.price == add_price_data[0].price for result in all_result)
