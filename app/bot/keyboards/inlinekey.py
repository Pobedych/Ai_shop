from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_menu():
    inline_kb = [
        [InlineKeyboardButton(text="Shop", callback_data="shop")],
        [InlineKeyboardButton(text="My Balance", callback_data="my_balance")],
        [InlineKeyboardButton(text="Settings", callback_data="settings")],
        [InlineKeyboardButton(text="About", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def language_menu(current_locale: str | None = None):
    en_text = "English"
    ru_text = "Russian"

    if current_locale == "en":
        en_text = "English (selected)"
    elif current_locale == "ru":
        ru_text = "Russian (selected)"

    inline_kb = [
        [InlineKeyboardButton(text=en_text, callback_data="set_lang:en")],
        [InlineKeyboardButton(text=ru_text, callback_data="set_lang:ru")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

