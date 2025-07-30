from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from create_bot import dp
from keyboards.inline import products_keyboard, rating_keyboard
from states import States

router = Router()


@dp.message(States.variant)
async def handle_variant(message: Message, state: FSMContext):
    variant = message.text.strip()
    await state.update_data(variant=variant)
    await state.set_state(States.flavor)
    await message.answer("Enter flavor:")


@router.callback_query(F.data.contains('skip.variant'))
async def skip_variant(callback: CallbackQuery, state: FSMContext):
    await state.update_data(set_state=States.comment_arina)
    await callback.message.edit_text("Arina:", reply_markup=rating_keyboard('arina'))


@dp.callback_query(F.data == "back.from.variant")
async def back_from_variant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data.get("category", "")
    await state.set_state(States.product)
    await callback.message.edit_text(
        text=category,
        reply_markup=products_keyboard(category)
    )
