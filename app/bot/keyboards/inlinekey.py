from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_i18n import I18nContext

from app.backend.models.item import Item


def start_menu(i18n: I18nContext):
    inline_kb = [
        [InlineKeyboardButton(text=i18n.get("shop_button"), callback_data="shop")],
        [
            InlineKeyboardButton(
                text=i18n.get("balance_button"), callback_data="my_balance"
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("settings_button"), callback_data="settings"
            )
        ],
        [InlineKeyboardButton(text=i18n.get("about_button"), callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def settings_menu(i18n: I18nContext):
    inline_kb = [
        [
            InlineKeyboardButton(
                text=i18n.get("set_language_button"), callback_data="set_language"
            )
        ],
        [
            InlineKeyboardButton(
                text=i18n.get("about_me_button"), callback_data="about_me"
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def language_menu(i18n: I18nContext, current_locale: str | None = None):
    en_text = i18n.get("language-name-en")
    ru_text = i18n.get("language-name-ru")
    zh_text = i18n.get("language-name-zh")

    if current_locale == "en":
        en_text = i18n.get("language-selected", name=en_text)
    elif current_locale == "ru":
        ru_text = i18n.get("language-selected", name=ru_text)
    elif current_locale == "zh":
        zh_text = i18n.get("language-selected", name=zh_text)

    inline_kb = [
        [InlineKeyboardButton(text=en_text, callback_data="set_lang:en")],
        [InlineKeyboardButton(text=ru_text, callback_data="set_lang:ru")],
        [InlineKeyboardButton(text=zh_text, callback_data="set_lang:zh")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def top_up_menu(i18n: I18nContext):
    inline_kb = [
        [
            InlineKeyboardButton(
                text=i18n.get("payment-method-cryptobot"), callback_data="pay"
            ),
            InlineKeyboardButton(
                text=i18n.get("payment-method-xrocket"), callback_data="pay"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


def categories_menu(categories: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=category, callback_data=f"category:{category}")]
        for category in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def items_menu(items: list[Item]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=item.name, callback_data=f"item:{item.id}")]
        for item in items
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
