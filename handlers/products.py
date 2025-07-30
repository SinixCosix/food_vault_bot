from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline import categories_keyboard
from keyboards.inline import skip_keyboard, rating_keyboard
from states import States

router = Router()


@router.message(F.text.lower().endswith('new'))
async def new_product(message: Message):
    await message.answer("Select category:", reply_markup=categories_keyboard())


@router.callback_query(F.data.contains('select_product'))
async def select_product(callback: CallbackQuery, state: FSMContext):
    product = callback.data.split('.')[1]
    await state.update_data(product=product)
    await state.set_state(States.variant)
    await callback.message.edit_text(
        "Enter variant:",
        reply_markup=skip_keyboard("skip.variant", "back.from.variant")
    )


