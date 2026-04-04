from unittest.mock import AsyncMock

import pytest

from app.backend.models.user import User
from app.bot.handlers.start import set_language


class DummyI18n:
    locale = "en"

    def __init__(self) -> None:
        self.set_locale = AsyncMock()

    def get(self, key: str, **kwargs) -> str:
        return key


def make_user() -> User:
    return User(
        tg_id=123456,
        username="alice",
        first_name="Alice",
        last_name="Doe",
        email=None,
        phone=None,
        role="USER",
        balance=0,
        purchase_count=0,
    )


@pytest.mark.asyncio
async def test_set_language_rejects_unsupported_locale() -> None:
    cq = AsyncMock()
    cq.data = "set_lang:de"
    i18n = DummyI18n()

    await set_language(
        cq=cq,
        i18n=i18n,
        db_user=make_user(),
        session=AsyncMock(),
    )

    i18n.set_locale.assert_not_awaited()
    cq.answer.assert_awaited_once_with("unsupported-language", show_alert=True)
    cq.message.edit_text.assert_not_awaited()


@pytest.mark.asyncio
async def test_set_language_updates_locale_and_edits_message() -> None:
    cq = AsyncMock()
    cq.data = "set_lang:ru"
    i18n = DummyI18n()

    await set_language(
        cq=cq,
        i18n=i18n,
        db_user=make_user(),
        session=AsyncMock(),
    )

    i18n.set_locale.assert_awaited_once_with("ru")
    cq.answer.assert_awaited_once_with("language-switched")
    cq.message.edit_text.assert_awaited_once()
