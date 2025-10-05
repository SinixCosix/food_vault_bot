import pytest
from unittest.mock import AsyncMock, patch

from bot.utils.api_client import APIClient


class TestAPIClientIntegration:
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        create_response = {'id': 1, 'category': 'Energy Drink', 'variant': 'Monster'}
        rating_response = {'message': 'Rating created', 'rating': 8}
        comment_response = {'message': 'Comment added', 'comment_id': 1}

        with patch('aiohttp.ClientSession.request') as mock_request:
            # Create three response context managers
            resp1 = AsyncMock()
            resp1.status = 201
            resp1.json = AsyncMock(return_value=create_response)
            resp2 = AsyncMock()
            resp2.status = 201
            resp2.json = AsyncMock(return_value=rating_response)
            resp3 = AsyncMock()
            resp3.status = 201
            resp3.json = AsyncMock(return_value=comment_response)

            # Each call to request returns an object with __aenter__ that yields the response
            cm1 = AsyncMock()
            cm1.__aenter__.return_value = resp1
            cm2 = AsyncMock()
            cm2.__aenter__.return_value = resp2
            cm3 = AsyncMock()
            cm3.__aenter__.return_value = resp3

            mock_request.side_effect = [cm1, cm2, cm3]

            async with APIClient() as client:
                product = await client.create_product(
                    category='Energy Drink',
                    variant='Monster',
                    telegram_id=123456789
                )
                assert product['id'] == 1

                rating = await client.add_rating(1, 123456789, 8)
                assert rating['rating'] == 8

                comment = await client.add_comment(1, 123456789, 'Great!')
                assert comment['comment_id'] == 1

                assert mock_request.call_count == 3


