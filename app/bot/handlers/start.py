from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext, LazyFilter
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from app.backend.core.config import SUPPORT_ACCOUNT, TG_CHANNEL
from app.backend.models.user import User
from app.backend.utils.convert import converted_currency
from app.bot.fsm.settings_fsm import Refill
from app.bot.keyboards.inlinekey import (
    language_menu,
    settings_menu,
    start_menu,
    top_up_menu,
)
from app.bot.keyboards.replykey import up_balance_kb, home

router = Router()


@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext, db_user: User):
    try:
        await message.answer(
            i18n.get(
                "start-welcome",
                id=str(message.from_user.id),
                balance=db_user.balance,
                usd_balance=await converted_currency("rub", "usd", db_user.balance),
                tg_chanel=TG_CHANNEL,
                account=SUPPORT_ACCOUNT,
            ),
            reply_markup=start_menu(i18n),
        )
    except :
        await message.answer()


# explain Пополнение баланса
# fixme заглушка
@router.message(LazyFilter("up-balance"))
async def up_balance(message: Message, i18n: I18nContext):
    await message.answer(
        text=i18n.get("choose-top-up-balance"), reply_markup=top_up_menu(i18n)
    )


@router.callback_query(F.data == "pay")
async def pay(cq: CallbackQuery, i18n: I18nContext, state: FSMContext):
    await cq.answer()
    await state.set_state(Refill.money)
    await cq.message.answer(text=i18n.get("top-up-enter-amount"))


@router.message(F.text & Refill.money)
async def money(
    message: Message,
    i18n: I18nContext,
    state: FSMContext,
    db_user: User,
    session: AsyncSession,
):
    raw_amount = message.text.strip()

    try:
        amount = int(raw_amount)
    except ValueError:
        await message.answer(i18n.get("top-up-invalid-amount"))
        return

    if amount <= 0:
        await message.answer(i18n.get("top-up-amount-positive"))
        return

    db_user.balance += Decimal(str(amount))
    await session.commit()

    await message.answer(i18n.get("top-up-success", balance=db_user.balance))
    await state.clear()


# explain О нас
@router.callback_query(F.data == "about")
async def about(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    await cq.message.answer(
        i18n.get("about-us", account=SUPPORT_ACCOUNT), reply_markup=home()
    )


# explain Настройки
@router.callback_query(F.data == "settings")
async def settings(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    await cq.message.answer(i18n.get("settings"), reply_markup=settings_menu(i18n))


# explain Мой баланс
@router.callback_query(F.data == "my_balance")
async def balance(cq: CallbackQuery, i18n: I18nContext, db_user: User):
    await cq.answer()
    await cq.message.answer(
        i18n.get(
            "balance-info",
            balance=db_user.balance,
            usd_balance=await converted_currency("rub", "usd", db_user.balance),
        ),
        reply_markup=up_balance_kb(i18n),
    )


# explain Настройки языка
@router.callback_query(F.data == "set_language")
async def open_language_settings(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    await cq.message.answer(
        i18n.get("language-prompt"), reply_markup=language_menu(i18n, i18n.locale)
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def set_language(
    cq: CallbackQuery, i18n: I18nContext, db_user: User, session: AsyncSession
):
    locale = cq.data.split(":")[1]
    if locale not in {"en", "ru", "zh"}:
        await cq.answer(i18n.get("unsupported-language"), show_alert=True)
        return

    await i18n.set_locale(locale)

    await cq.answer(i18n.get("language-switched"))
    await cq.message.edit_text(
        i18n.get("language-prompt"), reply_markup=language_menu(i18n, locale)
    )
