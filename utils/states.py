from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    login = State()
    email = State()
    password = State()

class Logging(StatesGroup):
    login = State()
    password = State()

class Info(StatesGroup):
    train = State()
    van = State()
    place = State()