from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from aiogram.exceptions import TelegramNetworkError

from app.backend.models.user import User
from app.bot.middleware import admin as admin_module


class DummyMessage:
    def __init__(self, user_id: int) -> None:
        self.from_user = SimpleNamespace(id=user_id)
        self.answer = AsyncMock()


class DummyCallbackQuery:
    def __init__(self, user_id: int) -> None:
        self.from_user = SimpleNamespace(id=user_id)
        self.answer = AsyncMock()


class DummySessionContext:
    def __init__(self, session: object) -> None:
        self.session = session

    async def __aenter__(self) -> object:
        return self.session

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


def make_user(role: str) -> User:
    return User(
        tg_id=123456,
        username="alice",
        first_name="Alice",
        last_name="Doe",
        email=None,
        phone=None,
        role=role,
        balance=0,
        purchase_count=0,
    )


@pytest.mark.asyncio
async def test_admin_middleware_blocks_non_admin_message_without_extra_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(admin_module, "Message", DummyMessage)
    monkeypatch.setattr(admin_module, "CallbackQuery", DummyCallbackQuery)
    get_user = AsyncMock()
    monkeypatch.setattr(admin_module, "get_user", get_user)

    middleware = admin_module.AdminMiddleware()
    handler = AsyncMock()
    event = DummyMessage(user_id=1)
    data = {"db_user": make_user("USER")}

    result = await middleware(handler, event, data)

    assert result is None
    handler.assert_not_awaited()
    get_user.assert_not_awaited()
    event.answer.assert_awaited_once_with("Access Denied")


@pytest.mark.asyncio
async def test_admin_middleware_blocks_non_admin_callback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(admin_module, "Message", DummyMessage)
    monkeypatch.setattr(admin_module, "CallbackQuery", DummyCallbackQuery)
    monkeypatch.setattr(
        admin_module, "SessionLocal", lambda: DummySessionContext(object())
    )
    monkeypatch.setattr(admin_module, "get_user", AsyncMock(return_value=None))

    middleware = admin_module.AdminMiddleware()
    handler = AsyncMock()
    event = DummyCallbackQuery(user_id=1)

    result = await middleware(handler, event, {})

    assert result is None
    handler.assert_not_awaited()
    event.answer.assert_awaited_once_with("Access Denied", show_alert=True)


@pytest.mark.asyncio
async def test_admin_middleware_allows_admin_and_passes_user_without_extra_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    admin_user = make_user("ADMIN")
    monkeypatch.setattr(admin_module, "Message", DummyMessage)
    monkeypatch.setattr(admin_module, "CallbackQuery", DummyCallbackQuery)
    get_user = AsyncMock()
    monkeypatch.setattr(admin_module, "get_user", get_user)

    middleware = admin_module.AdminMiddleware()
    handler = AsyncMock(return_value="ok")
    event = DummyMessage(user_id=1)
    data: dict[str, object] = {"db_user": admin_user}

    result = await middleware(handler, event, data)

    assert result == "ok"
    assert data["user"] is admin_user
    get_user.assert_not_awaited()
    handler.assert_awaited_once_with(event, data)


@pytest.mark.asyncio
async def test_admin_middleware_swallows_network_error_on_denial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(admin_module, "Message", DummyMessage)
    monkeypatch.setattr(admin_module, "CallbackQuery", DummyCallbackQuery)
    get_user = AsyncMock()
    monkeypatch.setattr(admin_module, "get_user", get_user)

    middleware = admin_module.AdminMiddleware()
    handler = AsyncMock()
    event = DummyMessage(user_id=1)
    event.answer = AsyncMock(
        side_effect=TelegramNetworkError(method=AsyncMock(), message="network down")
    )
    data = {"db_user": None}

    result = await middleware(handler, event, data)

    assert result is None
    handler.assert_not_awaited()
    get_user.assert_awaited_once()
    event.answer.assert_awaited_once_with("Access Denied")


@pytest.mark.asyncio
async def test_admin_middleware_uses_existing_session_as_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(admin_module, "Message", DummyMessage)
    monkeypatch.setattr(admin_module, "CallbackQuery", DummyCallbackQuery)
    session = object()
    fetched_user = make_user("ADMIN")
    get_user = AsyncMock(return_value=fetched_user)
    monkeypatch.setattr(admin_module, "get_user", get_user)

    middleware = admin_module.AdminMiddleware()
    handler = AsyncMock(return_value="ok")
    event = DummyMessage(user_id=42)
    data: dict[str, object] = {"session": session}

    result = await middleware(handler, event, data)

    assert result == "ok"
    assert data["user"] is fetched_user
    get_user.assert_awaited_once_with(session, 42)
    handler.assert_awaited_once_with(event, data)
