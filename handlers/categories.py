from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import products_keyboard
from states import States

router = Router()


@router.callback_query(F.data.contains('select_category'))
async def select_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split('.')[1]
    await state.update_data(category=category)
    await state.set_state(States.product)
    await callback.message.edit_text(text=state.next.text, )
