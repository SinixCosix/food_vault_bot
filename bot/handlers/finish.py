from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.inline import finish_keyboard
from bot.utils.format import format_product

router = Router()


@router.callback_query(F.data == "finish")
async def handle_finish(callback: CallbackQuery, state: FSMContext):
    await finish(callback, state)


async def finish(message_or_callback, state: FSMContext):
    product = await state.get_data()
    await state.clear()

    text = format_product(product)
    message = message_or_callback.message or message_or_callback
    await message.answer(text, reply_markup=finish_keyboard())

