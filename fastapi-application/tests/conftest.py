import asyncio

from collections.abc import AsyncGenerator
from datetime import UTC, datetime, timedelta

import pytest

from core.models.base import Base
from core.models.db_helper import db_helper
from core.schemas.prices import PriceCreate
from crud import prices as crud_prices
from httpx import AsyncClient
from main import main_app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool


DATABASE_URL_TEST = 'postgresql+asyncpg://user:password@pg:5432/test_db'

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


main_app.dependency_overrides[db_helper.session_getter] = override_get_async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=main_app, base_url='http://127.0.0.1:8000') as ac:
        yield ac


@pytest.fixture(scope='session')
async def async_session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as async_session:
        yield async_session


@pytest.fixture(scope='module')
async def add_price_data(async_session_fixture) -> AsyncGenerator[list[PriceCreate], None]:
    async with async_session_fixture as session:
        prices_data = [
            PriceCreate(ticker='BTC_USD', price=61300.34, timestamp=datetime.now(UTC)),
            PriceCreate(ticker='ETH_USD', price=850.21, timestamp=datetime.now(UTC)),
            PriceCreate(ticker='BTC_USD', price=61400.42, timestamp=datetime.now(UTC)),
            PriceCreate(ticker='ETH_USD', price=860.37, timestamp=datetime.now(UTC)),
            PriceCreate(ticker='BTC_USD', price=61500.96, timestamp=datetime.now(UTC) - timedelta(days=1)),
            PriceCreate(ticker='ETH_USD', price=870.34, timestamp=datetime.now(UTC) - timedelta(days=1)),
        ]

        for price_data in prices_data:
            await crud_prices.add_price(session, price_data)
        await session.commit()

        yield prices_data
