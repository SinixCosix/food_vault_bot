import pytest
from unittest.mock import AsyncMock, patch

from bot.utils.api_client import create_product_from_bot_data, save_rating_from_bot, save_comment_from_bot


class TestConvenienceFunctions:
    @pytest.mark.asyncio
    async def test_create_product_from_bot_data_success(self):
        bot_data = {
            'category': 'Energy Drink',
            'variant': 'Monster',
            'telegram_id': 123456789,
            'username': 'testuser',
            'flavors': ['Original'],
            'groups': ['Family']
        }
        expected_response = {'id': 1, 'category': 'Energy Drink'}
        with patch('bot.utils.api_client.APIClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.create_product.return_value = expected_response
            mock_client_class.return_value.__aenter__.return_value = mock_client
            result = await create_product_from_bot_data(bot_data)
            assert result == expected_response
            mock_client.create_product.assert_called_once_with(
                category='Energy Drink',
                variant='Monster',
                telegram_id=123456789,
                username='testuser',
                flavors=['Original'],
                groups=['Family']
            )

    @pytest.mark.asyncio
    async def test_save_rating_from_bot_success(self):
        expected_response = {'message': 'Rating saved', 'rating': 8}
        with patch('bot.utils.api_client.APIClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.add_rating.return_value = expected_response
            mock_client_class.return_value.__aenter__.return_value = mock_client
            result = await save_rating_from_bot(1, 123456789, 8)
            assert result == expected_response
            mock_client.add_rating.assert_called_once_with(1, 123456789, 8)

    @pytest.mark.asyncio
    async def test_save_comment_from_bot_success(self):
        expected_response = {'message': 'Comment saved', 'comment_id': 1}
        with patch('bot.utils.api_client.APIClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.add_comment.return_value = expected_response
            mock_client_class.return_value.__aenter__.return_value = mock_client
            result = await save_comment_from_bot(1, 123456789, 'Great product!')
            assert result == expected_response
            mock_client.add_comment.assert_called_once_with(1, 123456789, 'Great product!')

    @pytest.mark.asyncio
    async def test_convenience_functions_with_errors(self):
        with patch('bot.utils.api_client.APIClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.create_product.side_effect = Exception("API Error")
            mock_client_class.return_value.__aenter__.return_value = mock_client
            with pytest.raises(Exception, match="API Error"):
                await create_product_from_bot_data({'category': 'Test'})


