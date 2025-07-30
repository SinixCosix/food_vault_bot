from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from create_bot import storage


def skip_keyboard(callback_data: str = "skip", back_data: str = None):
    builder = InlineKeyboardBuilder()
    if back_data:
        builder.button(text=" ⬅️ Back ", callback_data=back_data)

    builder.button(text=" ⏭ Skip ", callback_data=callback_data)
    builder.adjust(2)

    return builder.as_markup()


def categories_keyboard():
    kb_list = [[InlineKeyboardButton(text=category, callback_data=f'select_category.{category}')]
               for category in storage['categories']
               ]

    kb_list.append([
        InlineKeyboardButton(text="+ New", callback_data='new_category'),
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def products_keyboard(category):
    kb_list = [[InlineKeyboardButton(text=product, callback_data=f'select_product.{product}')]
               for product in storage['products']
               ]
    kb_list.append([
        InlineKeyboardButton(text="⬅️ Back", callback_data=f'new.entry'),
        InlineKeyboardButton(text="+ New", callback_data='new_product'),
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb_list)


def rating_keyboard(user: str):
    builder = InlineKeyboardBuilder()
    button_labels = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    for i, label in enumerate(button_labels, start=1):
        builder.button(text=f'  {label}  ', callback_data=f"rate.{user}.{i}")

    builder.button(text="⬅️ Back", callback_data=f'back.from.rating.{user}')
    builder.adjust(5, 5, 2)

    return builder.as_markup()


def finish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏ Edit", callback_data="action.edit"),
            InlineKeyboardButton(text="+ New", callback_data="action.new"),
        ]
    ])
