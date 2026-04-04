from typing import Optional
from aiogram.types import User as TgUser
from aiogram_i18n.managers import BaseManager
from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.models.user import User as DbUser


class UserManager(BaseManager):
    async def get_locale(
        self, event_from_user: TgUser, db_user: Optional[DbUser] = None
    ) -> str:
        """
        Достает язык из объекта пользователя, который уже есть в системе.
        """
        if db_user:
            return db_user.language
        return self.default_locale

    async def set_locale(
        self,
        locale: str,
        event_from_user: TgUser,
        db_user: Optional[DbUser],
        session: AsyncSession,
    ) -> None:
        """
        Обновляет язык в базе данных. Коммитит изменения через активную сессию.
        """
        if db_user:
            db_user.language = locale
            await session.commit()
