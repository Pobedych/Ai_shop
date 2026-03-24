from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from app.backend.core.config import SUPPORT_ACCOUNT, TG_CHANNEL
from app.backend.core.database import SessionLocal
from app.backend.services.user_service import get_or_create_user, get_user
from app.backend.utils.convert import converted_currency

from app.bot.keyboards.inlinekey import language_menu, start_menu, settings_menu, top_up_menu
from app.bot.keyboards.replykey import up_balance_kb
from app.bot.filter.settings_fsm import Refill

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
    await i18n.set_locale(db_user.language)
    await message.answer(
        i18n.get(
            "start-welcome",
            id=str(tg_user.id),
            balance=db_user.balance,
            usd_balance=await converted_currency('rub', 'usd', db_user.balance),
            tg_chanel=TG_CHANNEL,
            account=SUPPORT_ACCOUNT,
        ),
        reply_markup=start_menu(i18n),
    )


@router.message(F.text == '💳 Top up your balance now' or '💳 Пополнить баланс')
async def up_balance(message: Message, i18n: I18nContext):
    await message.answer(text=i18n.get('choose-top-up-balance'), reply_markup=top_up_menu())


@router.callback_query(F.data == 'pay')
async def pay(cq: CallbackQuery, i18n: I18nContext, state: FSMContext ):
    await cq.answer()
    await state.set_state(Refill.money)
    await cq.message.answer(text='Введите сумму которую хотите положить')


@router.message(Refill.money)
async def money(message: Message, i18n: I18nContext, state: FSMContext):
    await state.update_data(money=message.text)
    data = await state.get_data()
    async with SessionLocal() as session:
        db_user = await get_user(db=session, tg_id=message.from_user.id)
        if db_user is None:
            await cq.message.edit_text("User not found. Send /start first.")
            return
        db_user.balance += int(data['money'])
        await session.commit()
    await message.answer(text=f'Баланс пополнен {db_user.balance}')


#CALLBACK SHOP
@router.callback_query(F.data == 'shop')
async def shop(cq: CallbackQuery):
    await cq.answer()
    await cq.message.answer("Shop is not implemented yet.")


#CALLBACK SETTINGS
@router.callback_query(F.data == 'settings')
async def settings(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    await cq.message.answer(i18n.get('settings'), reply_markup=settings_menu(i18n))


#CALLBACK BALANCE
@router.callback_query(F.data == 'my_balance')
async def balance(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    async with SessionLocal() as session:
        db_user = await get_user(db=session, tg_id=cq.from_user.id)
    if db_user is None:
        await cq.message.edit_text("User not found. Send /start first.")
        return
    await cq.message.answer(
        i18n.get(
            'balance-info',
            balance=db_user.balance,
            usd_balance=await converted_currency('rub', 'usd', db_user.balance),
        ),
        reply_markup=up_balance_kb(i18n),
    )


#CALLBACK SET LANGUAGE
@router.callback_query(F.data == 'set_language')
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

    async with SessionLocal() as session:
        db_user = await get_user(db=session, tg_id=cq.from_user.id)
        if db_user is None:
            await cq.answer("User not found. Send /start first.", show_alert=True)
            return

        db_user.language = locale
        await session.commit()

    await i18n.set_locale(locale)

    notice = "Language switched to English." if locale == "en" else "Язык переключен на русский."
    prompt = "Choose language:" if locale == "en" else "Выберите язык:"

    await cq.answer(notice)
    await cq.message.edit_text(prompt, reply_markup=language_menu(locale))
