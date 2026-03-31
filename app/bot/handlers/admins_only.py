from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command
from app.bot.middleware.admin import AdminMiddleware


admin_router = Router()
admin_router.message.middleware(AdminMiddleware())

@admin_router.message(Command("admin"))
async def admin(message: Message):
    await message.answer("Admin panel")