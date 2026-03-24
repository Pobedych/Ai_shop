from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_i18n import I18nContext

def up_balance_kb(i18n: I18nContext):
    balance = [
        [KeyboardButton(text=i18n.get('up-balance'))]
    ]
    return ReplyKeyboardMarkup(keyboard=balance, resize_keyboard=True, one_time_keyboard=True)
