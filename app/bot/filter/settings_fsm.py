from aiogram.fsm.state import State, StatesGroup

class Captcha(StatesGroup):
    captcha = State()

class Refill(StatesGroup):
    money = State()