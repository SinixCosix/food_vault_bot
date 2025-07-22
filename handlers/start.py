from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.all_keyboards import main_keyboard
from keyboards.inline_keyboards import categories_keyboard, products_keyboard, rating_keyboard
from create_bot import logger, AddTaste, dp

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text='Started',
        reply_markup=main_keyboard()
    )


@start_router.message(F.text == "➕ Add")
async def handle_add(message: Message):
    await message.answer(
        text='Select category',
        reply_markup=categories_keyboard()
    )


@start_router.callback_query(F.data.contains('select_category'))
async def select_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split('.')[1]
    await state.update_data(category=category)
    await state.set_state(AddTaste.product)

    await callback.message.edit_text(
        text=category,
        reply_markup=products_keyboard(category)
    )


@start_router.callback_query(F.data.contains('select_product'))
async def select_product(callback: CallbackQuery, state: FSMContext):
    product = callback.data.split('.')[1]
    await state.update_data(product=product)
    await state.set_state(AddTaste.rating_andrew)

    await callback.message.edit_text(
        "Andrew:",
        reply_markup=rating_keyboard('andrew')
    )


@dp.callback_query(F.data.startswith("rate.andrew."))
async def rate_andrei(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(".")[-1])
    await state.update_data(rating_andrei=rating)
    await state.set_state(AddTaste.rating_arina)
    await callback.message.edit_text("Arina:", reply_markup=rating_keyboard("arina"))


@dp.callback_query(F.data.startswith("rate.arina."))
async def rate_arina(callback: CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(".")[-1])
    data = await state.get_data()

    await state.clear()
    await callback.message.edit_text(
        f"({data['category']} -- {data['product']}\n"
        f"🌵 Andrew: {data['rating_andrei']}/10\n"
        f"🦖 Arina: {rating}/10"
    )
