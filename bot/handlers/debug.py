from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from datetime import datetime

from bot.keyboards.reply import main_keyboard
from bot.utils.api_client import create_product_from_bot_data

router = Router()


@router.message(F.text == 'debug-add-product')
async def debug(message: Message):
    try:
        product_data = {
            'category': f'tmp-category-{datetime.now().timestamp()}',
            'variant': 'some',
            'telegram_id': 1,
            'username': 'testuser',
            'flavors': ['Original', 'Zero'],
            'groups': ['Family', 'Friends'],
            'ratings': [
                {'telegram_id': 1, 'rating': 9},
                {'telegram_id': 2, 'rating': 7},
            ],
            'comments': [
                {'telegram_id': 1, 'comment': 'Great!'},
                {'telegram_id': 2, 'comment': 'Nice'},
            ]
        }
        api_response = await create_product_from_bot_data(product_data)
        await message.answer(f"Debug product saved!")
    except Exception as e:
        await message.answer(f"⚠️ Product created locally (API error: {str(e)})")