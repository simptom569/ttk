from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def get_menu(train: str, van: str, place: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Открыть меню", web_app=WebAppInfo(url=f"https://2875-2a03-d000-1608-a17d-7d77-a1b0-a761-e021.ngrok-free.app?train={train}&van={van}&place={place}")),
            ]
        ]
    )

    return keyboard