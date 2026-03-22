from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from app.backend.core.config import SUPPORT_ACCOUNT, TG_CHANNEL
from app.backend.core.database import SessionLocal
from app.backend.services.auth import get_or_create_user
from app.backend.utils.convert import converted_currency

from app.bot.keyboards.inlinekey import language_menu, start_menu

router = Router()

#START BOT
@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext):
    tg_user = message.from_user
    async with SessionLocal() as session:
        db_user, _created = await get_or_create_user(
            db=session,
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            phone=None,
            email=None,
        )
    await message.answer(
        i18n.get(
            "start-welcome",
            id=str(tg_user.id),
            balance=db_user.balance,
            usd_balance=0 , #converted_currency("rub", "usd", db_user.balance)
            tg_chanel=TG_CHANNEL,
            account=SUPPORT_ACCOUNT,
        ),
        reply_markup=start_menu(),
    )


#CALLBACK
@router.callback_query(F.data == 'shop')
async def shop(cq: CallbackQuery):
    await cq.answer()
    await cq.message.answer("Shop is not implemented yet.")


@router.callback_query(F.data == 'settings')
async def settings(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()

    prompt = "Choose language:" if i18n.locale == "en" else "Выберите язык:"
    await cq.message.answer(prompt, reply_markup=language_menu(i18n.locale))


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(cq: CallbackQuery, i18n: I18nContext):
    locale = cq.data.split(":", maxsplit=1)[1]
    if locale not in {"en", "ru"}:
        await cq.answer("Unsupported language", show_alert=True)
        return

    await i18n.set_locale(locale)

    notice = "Language switched to English." if locale == "en" else "Язык переключен на русский."
    prompt = "Choose language:" if locale == "en" else "Выберите язык:"

    await cq.answer(notice)
    await cq.message.edit_text(prompt, reply_markup=language_menu(locale))



