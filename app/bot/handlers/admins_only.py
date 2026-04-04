from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from app.bot.middleware.admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())
admin_router.callback_query.middleware(AdminMiddleware())


@admin_router.message(Command("admin"))
async def admin(message: Message):
    await message.answer("Admin panel")
