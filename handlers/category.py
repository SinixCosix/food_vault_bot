from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import States

router = Router()


@router.message(F.text.lower().endswith('new'))
async def handle_message(message: Message, state: FSMContext):
    await state.set_state(States.category)
    await message.answer(text=States.category.text, reply_markup=States.category.keyboard)


@router.callback_query(F.data.contains('go.to.category'))
async def handle_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(States.category)
    await callback.message.edit_text(text=States.category.text, reply_markup=States.category.keyboard)


@router.callback_query(F.data.contains('select.category'))
async def select(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split('.')[-1]
    await state.update_data(category=category)

    await state.set_state(States.variant)
    await callback.message.edit_text(text=States.variant.text, reply_markup=States.variant.keyboard)


@router.message(States.category)
async def create(message: Message, state: FSMContext):
    category = message.text.strip()
    await state.update_data(category=category)

    await state.set_state(States.variant)
    await message.answer(text=States.variant.text, reply_markup=States.variant.keyboard)
