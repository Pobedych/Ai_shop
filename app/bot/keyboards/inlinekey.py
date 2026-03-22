from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_menu():
    inline_kb = [
        [InlineKeyboardButton(text="Shop", callback_data="shop")],
        [InlineKeyboardButton(text="My Balance", callback_data="my_balance")],
        [InlineKeyboardButton(text="Settings", callback_data="settings")],
        [InlineKeyboardButton(text="About", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

