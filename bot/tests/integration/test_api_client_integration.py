import pytest
from unittest.mock import AsyncMock, patch, post

from bot.utils.api_client import APIClient


class TestAPIClientIntegration:
    @pytest.mark.asyncio
    async def test_create_product__filled_all_fields(self):
        with post('aiohttp.ClientSession.request') as mock_request:
            async with APIClient() as client:
                product = await client.create_product(
                    category='Energy Drink',
                    variant='Monster',
                    telegram_id=123456789,
                )
                assert product['id'] == 1

                rating = await client.add_rating(1, 123456789, 8)
                assert rating['rating'] == 8

                comment = await client.add_comment(1, 123456789, 'Great!')
                assert comment['comment_id'] == 1

                assert mock_request.call_count == 3


