from aiogram import Bot, Dispatcher

from handlers import command_handler, login_handler, document_handler, document_callback_handler, pay_handler

import asyncio
import logging
from sys import stdout

from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(
        command_handler.dp,
        login_handler.dp,
        document_handler.dp,
        document_callback_handler.dp,
        pay_handler.dp,
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")