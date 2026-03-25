from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext


def start_menu(i18n: I18nContext):
    inline_kb = [
        [InlineKeyboardButton(text=i18n.get('shop_button'), callback_data="shop")],
        [InlineKeyboardButton(text=i18n.get('balance_button'), callback_data="my_balance")],
        [InlineKeyboardButton(text=i18n.get('settings_button'), callback_data="settings")],
        [InlineKeyboardButton(text=i18n.get('about_button'), callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

def settings_menu(i18n: I18nContext):
    inline_kb = [
        [InlineKeyboardButton(text=i18n.get('set_language_button'), callback_data="set_language")],
        [InlineKeyboardButton(text=i18n.get('about_me_button'), callback_data="about_me")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

def language_menu(current_locale: str | None = None):
    en_text = "English"
    ru_text = "Russian"
    zh_text = "Chinese"

    if current_locale == "en":
        en_text = "English (selected)"
    elif current_locale == "ru":
        ru_text = "Russian (selected)"
    elif current_locale == "zh":
        zh_text = "Chinese (selected)"

    inline_kb = [
        [InlineKeyboardButton(text=en_text, callback_data="set_lang:en")],
        [InlineKeyboardButton(text=ru_text, callback_data="set_lang:ru")],
        [InlineKeyboardButton(text=zh_text, callback_data="set_lang:zh")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)

#FIX IN MVP ADD REAL PAYMENTS METHOD
def top_up_menu():
    inline_kb = [
        [InlineKeyboardButton(text='CryptoBot 1.5% fee', callback_data='pay'), InlineKeyboardButton(text='XRocket 1% fee', callback_data="pay")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)
