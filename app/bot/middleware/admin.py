from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from app.backend.core.database import SessionLocal
from app.backend.services.user_service import get_user


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = event.from_user.id

        async with SessionLocal() as session:
            user = await get_user(session, user_id)

        if user is None or user.role != 'ADMIN':
            if isinstance(event, Message):
                await event.answer('Access Denied')
            elif isinstance(event, CallbackQuery):
                await event.answer('Access Denied', show_alert=True)
            return None

        data['user'] = user
        return await handler(event, data)
