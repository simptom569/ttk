from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def get_menu(train: str, van: str, place: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Открыть меню", web_app=WebAppInfo(url=f"https://fef8-87-117-49-169.ngrok-free.app?train={train}&van={van}&place={place}")),
            ]
        ]
    )

    return keyboard