from aiogram import Bot, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputMediaPhoto

from keyboards.keyboard_command import unlogged_keyboard
from utils import data


dp = Router()

@dp.message(CommandStart())
async def start_command(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, "Приветствую вас в нашем ТТК Боте:)")
    logged = await data.get_logged_user(message.from_user.id)
    if logged == False:
        await bot.send_message(message.from_user.id, "Для тест вы моежет использовать данные (27 поезд, 1 и 2 вагоны), а также фотографии нахоящиейсяя в корнейвой папке проекта")
        await bot.send_message(message.from_user.id, "Вы хотите войти или зарегестрироваться?", reply_markup=unlogged_keyboard())