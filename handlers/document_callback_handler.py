from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from keyboards import keyboard_pay, keyboard_command

import re


dp = Router()

@dp.callback_query(F.data == "yes")
async def document_yes(callback_query: CallbackQuery, bot: Bot):
    await callback_query.answer()
    train_number = re.search(r'поезд: (\d+)', callback_query.message.text).group(1)
    wagon_number = re.search(r'вагон: (\d+)', callback_query.message.text).group(1)
    seat_number = re.search(r'место: (\d+)', callback_query.message.text).group(1)
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Приятных покупок", reply_markup= keyboard_command.signout_keyboard())
    await bot.send_message(callback_query.from_user.id, "Вот ваше меню", reply_markup=keyboard_pay.get_menu(train_number, wagon_number, seat_number))

@dp.callback_query(F.data == "no")
async def document_no(callback_query: CallbackQuery, bot: Bot):
    await callback_query.answer()
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id, "Пришли фото паспорта или билета, или заполните вручную", reply_markup=keyboard_command.signout_keyboard())