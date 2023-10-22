from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards import keyboard_document
from utils.filters import IsPDF, IsLogged
from utils.data import get_user_ticket_info
from utils.states import Info
from vision.main import get_text


dp = Router()

@dp.message(F.document, IsPDF(), IsLogged())
async def download_pdf(message: Message, bot: Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    file_path  = file.file_path
    await bot.download_file(f"{file_path}", f"documents/{message.document.file_unique_id}.{file_name.split('.')[-1]}")
    data = get_text(f"documents/{message.document.file_unique_id}.{file_name.split('.')[-1]}")
    if data["type"] == "pasport":
        data = await get_user_ticket_info(data["series_number"])
    await bot.send_message(message.from_user.id, f"Ваш поезд: {data['train']}\nВаш вагон: {data['van']}\nВаше место: {data['place']}", reply_markup=keyboard_document.check_data())

@dp.message(F.photo, IsLogged())
async def download_photo(message: Message, bot: Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    await bot.download_file(f"{file_path}", f"documents/{file.file_unique_id}.jpg")
    data = get_text(f"documents/{file.file_unique_id}.jpg")
    if data["type"] == "pasport":
        data = await get_user_ticket_info(data["series_number"])
    await bot.send_message(message.from_user.id, f"Ваш поезд: {data['train']}\nВаш вагон: {data['van']}\nВаше место: {data['place']}", reply_markup=keyboard_document.check_data())

@dp.message(F.text.lower() == "заполнить вручную", IsLogged())
async def write_info(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Info.train)
    await bot.send_message(message.from_user.id, "Введите номер поезда", reply_markup=ReplyKeyboardRemove())

@dp.message(Info.train)
async def write_info_train(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Info.van)
    await state.update_data(train=message.text)
    await bot.send_message(message.from_user.id, "Введитие номер вагона")

@dp.message(Info.van)
async def write_info_van(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Info.place)
    await state.update_data(van=message.text)
    await bot.send_message(message.from_user.id, "Введитие номер места")

@dp.message(Info.place)
async def write_info_place(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(place=message.text)
    data = await state.get_data()
    await state.clear()

    await bot.send_message(message.from_user.id, f"Ваш поезд: {data['train']}\nВаш вагон: {data['van']}\nВаше место: {data['place']}", reply_markup=keyboard_document.check_data())