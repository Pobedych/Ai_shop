from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.services.user_service import get_or_create_user, update_user_info
from app.bot.create_bot import admins


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: TgUser = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)

        # Получаем сессию из DbSessionMiddleware
        session: AsyncSession = data["session"]

        role = "ADMIN" if tg_user.id in admins else "USER"

        db_user, created = await get_or_create_user(
            db=session,
            tg_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            phone=None,
            email=None,
            role=role,
        )

        if not created:
            db_user = await update_user_info(
                db=session,
                user=db_user,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
                role=role,
            )

        data["db_user"] = db_user
        return await handler(event, data)
