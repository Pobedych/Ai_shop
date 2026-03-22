from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram_i18n import I18nContext

from app.bot.keyboards.inlinekey import start_menu

router = Router()

#START BOT
@router.message(CommandStart())
async def start(message: Message, i18n: I18nContext):
    await message.answer(i18n.get("start-welcome", id=message.from_user.id), reply_markup=start_menu())


#CALLBACK
@router.callback_query(F.data == 'shop')
async def shop(cq: CallbackQuery):
    await cq.answer()
    await cq.message.answer("Shop is not implemented yet.")




