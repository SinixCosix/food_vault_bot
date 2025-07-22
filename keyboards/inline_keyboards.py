from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from create_bot import storage


def categories_keyboard():
    kb_list = [[InlineKeyboardButton(text=category, callback_data=f'select_category.{category}')]
               for category in storage['categories']
               ]

    kb_list.append([
        InlineKeyboardButton(text="New...", callback_data='new_category'),
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def products_keyboard(category):
    kb_list = [[InlineKeyboardButton(text=product, callback_data=f'select_product.{product}')]
               for product in storage['products']
               ]
    kb_list.append([
        InlineKeyboardButton(text='Back', callback_data=f'select_category.{category}'),
        InlineKeyboardButton(text="New...", callback_data='new_product'),
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def rating_keyboard(user: str):
    builder = InlineKeyboardBuilder()
    for i in range(1, 11):
        builder.button(text=str(i), callback_data=f"rate.{user}.{i}")
    builder.adjust(5)
    return builder.as_markup()
