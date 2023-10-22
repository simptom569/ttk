from aiogram import Bot, Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from utils.filters import IsLogged
from utils.states import Logging, Registration
from utils.data import get_logging_user, create_user, delete_session
from keyboards import keyboard_command


dp = Router()

@dp.message(F.text.lower() == "войти", ~IsLogged())
async def sign_in(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Logging.login)
    await bot.send_message(message.from_user.id, "Веедите логин", reply_markup=ReplyKeyboardRemove())

@dp.message(Logging.login)
async def sign_in_login(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(Logging.password)
    await bot.send_message(message.from_user.id, "Введите пароль")

@dp.message(Logging.password)
async def sign_in_password(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await state.clear()

    logging_user = await get_logging_user(data["login"], data["password"], message.from_user.id)
    if logging_user:
        await bot.send_message(message.from_user.id, "Вы успешно вошли", reply_markup=keyboard_command.signout_keyboard())
    else:
        await bot.send_message(message.from_user.id, "Вход не был успешен", reply_markup=keyboard_command.unlogged_keyboard())

@dp.message(F.text.lower() == "зарегестрироваться", ~IsLogged())
async def sign_up(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(Registration.login)
    await bot.send_message(message.from_user.id, "Давайте же создадим страницу", reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, "Введите логин")

@dp.message(Registration.login)
async def sign_up_login(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(Registration.email)
    await bot.send_message(message.from_user.id, "Напишите свой email адресс")

@dp.message(Registration.email)
async def sign_up_email(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Registration.password)
    await bot.send_message(message.from_user.id, "Придумайте пароль")

@dp.message(Registration.password)
async def sign_up_password(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await state.clear()

    registration_user = await create_user(message.from_user.id, data["login"], data["password"])
    if registration_user:
        await bot.send_message(message.from_user.id, "Регистрация прошла успешна", reply_markup=keyboard_command.signout_keyboard())
    else:
        await bot.send_message(message.from_user.id, "Регистрация не была успешна", reply_markup=keyboard_command.unlogged_keyboard())

@dp.message(F.text.lower() == "выйти с аккаунта", IsLogged())
async def sign_out(message: Message, bot: Bot):
    await delete_session(message.from_user.id)
    await bot.send_message(message.from_user.id, "Вы успешно вышли с аккаунта", reply_markup=keyboard_command.unlogged_keyboard())