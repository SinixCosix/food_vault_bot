from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.all_keyboards import main_keyboard
from create_bot import logger

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Started',
        reply_markup=main_keyboard()
    )


@start_router.message(F.text.lower().contains('add'))
async def add_product(message: Message):
    logger.info(f'Adding product {message.text}')

