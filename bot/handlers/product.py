from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.states import States

router = Router()


@router.callback_query(F.data.contains('go.to.product'))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.product)
    await callback.message.edit_text(text=States.product.text, reply_markup=States.product.keyboard)


@router.message(States.product)
async def create(message: Message, state: FSMContext):
    value = message.text.strip()
    await state.update_data(product=value)

    await state.set_state(States.variant)
    await message.answer(text=States.variant.text, reply_markup=States.variant.keyboard)
