from datetime import UTC, datetime

from conftest import async_session_maker
from core.schemas.prices import PriceCreate
from crud import prices as crud_prices


async def test_add_price():
    async with async_session_maker() as session:
        price_data = PriceCreate(ticker='ETH_USD', price=12345.66, timestamp=datetime.now(UTC))
        await crud_prices.add_price(session, price_data)
        prices = await crud_prices.get_prices(session, ticker='ETH_USD')

        assert len(prices) == 1
        assert prices[0].ticker == 'ETH_USD'
        assert prices[0].price == 12345.66
