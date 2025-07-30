from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from create_bot import dp
from keyboards.inline import skip_keyboard
from states import States

router = Router()


@dp.callback_query(F.data.startswith("rate.arina."))
async def rate_arina(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(".")[-1])
    await state.update_data(rating_arina=rating)
    await state.set_state(States.comment_arina)
    await callback.message.edit_text(
        "Comment from Arina",
        reply_markup=skip_keyboard("skip.arina", "back.from.comment_arina")
    )


@dp.callback_query(F.data.startswith("back.from.rating."))
async def handle_back_rating(callback: CallbackQuery, state: FSMContext):
    prefix = callback.data.split('.')[-1]

    if prefix == "arina":
        await state.set_state(States.variant)
        await callback.message.edit_text("Enter variant:", reply_markup=skip_keyboard("skip.variant"))

    elif prefix == "andrew":
        await state.set_state(States.comment_arina)
        await callback.message.edit_text("Comment from Arina:", reply_markup=skip_keyboard("skip.arina"))
