from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_keyboard():
    kb_list = [
        [KeyboardButton(text="➕ New"),
         KeyboardButton(text="✏ Edit")],

        [KeyboardButton(text='🔁'), KeyboardButton(text="🔎 Search")]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    return keyboard
