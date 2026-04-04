import logging

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramNetworkError
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.database import SessionLocal
from app.backend.models.user import User
from app.backend.services.user_service import get_user


logger = logging.getLogger(__name__)


class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user: User | None = data.get("db_user")

        if user is None:
            user_id = event.from_user.id
            session: AsyncSession | None = data.get("session")

            if session is not None:
                user = await get_user(session, user_id)
            else:
                async with SessionLocal() as fallback_session:
                    user = await get_user(fallback_session, user_id)

        if user is None or user.role != "ADMIN":
            try:
                if isinstance(event, Message):
                    await event.answer("Access Denied")
                elif isinstance(event, CallbackQuery):
                    await event.answer("Access Denied", show_alert=True)
            except TelegramNetworkError:
                logger.warning("Failed to send admin denial message", exc_info=True)
            return None

        data["user"] = user
        return await handler(event, data)
