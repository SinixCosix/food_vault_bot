from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import dp
from handlers.finish import finish_entry
from keyboards.inline import rating_keyboard, skip_keyboard
from states import States

router = Router()


@dp.message(States.comment_arina)
async def comment_arina(message: Message, state: FSMContext):
    comment = message.text.strip()
    await state.update_data(comment_arina=comment)
    await state.set_state(States.rating_andrew)
    await message.answer("Andrew:", reply_markup=rating_keyboard("andrew"))


@dp.callback_query(F.data == "skip.arina")
async def skip_comment_arina(callback: CallbackQuery, state: FSMContext):
    await state.update_data(comment_arina=None)
    await state.set_state(States.rating_andrew)
    await callback.message.edit_text("Andrew — оценка от 1 до 10:", reply_markup=rating_keyboard("andrew"))


@dp.callback_query(F.data.startswith("rate.andrew."))
async def rate_andrew(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(".")[-1])
    await state.update_data(rating_andrew=rating)
    await state.set_state(States.comment_andrew)
    await callback.message.edit_text(
        "Comment from Andrew:",
        reply_markup=skip_keyboard("skip.andrew", "back.from.comment_andrew")
    )


@dp.callback_query(F.data == "skip.andrew")
async def skip_comment_andrew(callback: CallbackQuery, state: FSMContext):
    await state.update_data(comment_andrew=None)
    await finish_entry(callback.message, state)


@dp.message(States.comment_andrew)
async def comment_andrew(message: Message, state: FSMContext):
    comment = message.text.strip()
    await state.update_data(comment_andrew=comment)
    await finish_entry(message, state)


@dp.callback_query(F.data == "back.from.comment_arina")
async def back_from_comment_arina(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.rating_arina)
    await callback.message.edit_text("Arina:", reply_markup=rating_keyboard("arina"))


@dp.callback_query(F.data == "back.from.comment_andrew")
async def back_from_comment_andrew(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.rating_andrew)
    await callback.message.edit_text("Andrew:", reply_markup=rating_keyboard("andrew"))
