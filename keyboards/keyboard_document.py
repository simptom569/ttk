from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_data():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="да", callback_data="yes"),
                InlineKeyboardButton(text="нет", callback_data="no"),
            ]
        ]
    )

    return keyboard