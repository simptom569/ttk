from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def unlogged_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Войти"),
                KeyboardButton(text="Зарегестрироваться"),
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="↓Выберите способ входа↓"
    )

    return keyboard

def signout_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Заполнить вручную")
            ],
            [
                KeyboardButton(text="Выйти с аккаунта")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return keyboard