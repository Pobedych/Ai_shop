from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_kb():
    kb_list = [
        KeyboardButton(text="Shop"),
        KeyboardButton(text="My Balance"),
        KeyboardButton(text="Settings"),
        KeyboardButton(text="About"),
    ]