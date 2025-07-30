from aiogram import Router
from aiogram.fsm.context import FSMContext

from keyboards.inline import finish_keyboard
from keyboards.reply import main_keyboard

router = Router()


async def finish_entry(message_or_callback, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    text = (
        f"📂 {data['category']} — {data['product']} ({data.get('variant') or ''})\n\n"
        f"🦖 Arina: {data['rating_arina']}/10\n"
        f"💬 {data.get('comment_arina') or '—'}\n\n"
        f"🌵 Andrew: {data['rating_andrew']}/10\n"
        f"💬 {data.get('comment_andrew') or '—'}"
    )

    await message_or_callback.answer(text, reply_markup=finish_keyboard())
    await message_or_callback.answer("", reply_markup=main_keyboard())
