from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import finish_keyboard
from keyboards.reply import main_keyboard

router = Router()


@router.callback_query(F.data == "finish")
async def handle_finish(callback: CallbackQuery, state: FSMContext):
    await finish(callback, state)


async def finish(message_or_callback, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    fields = [data.get('category'), data.get('variant'), data.get('flavor')]

    text = (
        f"📂 {fields})\n\n"
        f"🦖 Arina: {data['rating_arina']}/10\n"
        f"💬 {data.get('comment_arina') or '—'}\n\n"
        f"🌵 Andrew: {data['rating_andrew']}/10\n"
        f"💬 {data.get('comment_andrew') or '—'}"
    )

    message = message_or_callback.message or message_or_callback
    await message.answer(text, reply_markup=finish_keyboard())
