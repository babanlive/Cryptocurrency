import asyncio
import logging
import time

from datetime import UTC, datetime

import aiohttp

from core.models import db_helper
from core.schemas.prices import PriceCreate
from crud import prices as crud_prices
from sqlalchemy.ext.asyncio import AsyncSession


API_URL = 'https://www.deribit.com/api/v2/public/get_index_price'
TIKERS_LIST = ['btc_usd', 'eth_usd']


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_index_price(session: aiohttp.ClientSession, course: str) -> dict:
    params = {'index_name': course}
    try:
        async with session.get(API_URL, params=params) as response:
            response.raise_for_status()
            data = await response.json()
            return {
                'ticker': course.upper(),
                'price': data['result']['index_price'],
                'timestamp': int(time.time()),
            }
    except aiohttp.ClientError as e:
        logger.error(f'Failed to get index price {course}: {e}')
        return None


async def get_and_save_prices():
    async with aiohttp.ClientSession() as session:
        tasks = [get_index_price(session, ticker) for ticker in TIKERS_LIST]
        prices = await asyncio.gather(*tasks)

    prices = [price for price in prices if price is not None]

    if not prices:
        logger.warning('No prices were fetched successfully')
        return

    async for db_session in db_helper.session_getter():
        await save_to_database(db_session, prices)


async def save_to_database(session: AsyncSession, prices: list[dict]):
    for price in prices:
        price_data = PriceCreate(
            ticker=price['ticker'],
            price=price['price'],
            timestamp=datetime.fromtimestamp(price['timestamp'], tz=UTC),
        )
        try:
            await crud_prices.add_price(session, price_data)
        except Exception as e:
            logger.error(f'Failed to save price {price_data.ticker} to database: {e}')


async def main():
    while True:
        try:
            await get_and_save_prices()
        except Exception as e:
            logger.error(f'Failed to get and save prices: {e}')
        await asyncio.sleep(60)


if __name__ == '__main__':
    asyncio.run(main())
