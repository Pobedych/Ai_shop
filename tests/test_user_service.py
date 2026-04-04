from unittest.mock import AsyncMock

import pytest
from sqlalchemy.exc import IntegrityError

from app.backend.models.user import User
from app.backend.services import user_service


def make_user(**overrides) -> User:
    payload = {
        "tg_id": 123456,
        "username": "alice",
        "first_name": "Alice",
        "last_name": "Doe",
        "email": None,
        "phone": None,
        "role": "USER",
        "balance": 0,
        "purchase_count": 0,
    }
    payload.update(overrides)
    return User(**payload)


@pytest.mark.asyncio
async def test_get_or_create_user_returns_existing_user_without_commit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock()
    existing_user = make_user()

    get_user = AsyncMock(return_value=existing_user)
    monkeypatch.setattr(user_service, "get_user", get_user)

    user, created = await user_service.get_or_create_user(
        db=session,
        tg_id=existing_user.tg_id,
        username=existing_user.username,
        first_name=existing_user.first_name,
        last_name=existing_user.last_name,
        phone=existing_user.phone,
        email=existing_user.email,
        role=existing_user.role,
    )

    assert user is existing_user
    assert created is False
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_or_create_user_registers_and_commits_new_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock()
    new_user = make_user()

    monkeypatch.setattr(user_service, "get_user", AsyncMock(return_value=None))
    register_user = AsyncMock(return_value=new_user)
    monkeypatch.setattr(user_service, "register_user", register_user)

    user, created = await user_service.get_or_create_user(
        db=session,
        tg_id=new_user.tg_id,
        username=new_user.username,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        phone=new_user.phone,
        email=new_user.email,
        role=new_user.role,
    )

    assert user is new_user
    assert created is True
    register_user.assert_awaited_once()
    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_or_create_user_recovers_after_integrity_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = AsyncMock()
    persisted_user = make_user()

    monkeypatch.setattr(
        user_service,
        "get_user",
        AsyncMock(side_effect=[None, persisted_user]),
    )
    monkeypatch.setattr(
        user_service,
        "register_user",
        AsyncMock(side_effect=IntegrityError("insert", {}, Exception("duplicate"))),
    )

    user, created = await user_service.get_or_create_user(
        db=session,
        tg_id=persisted_user.tg_id,
        username=persisted_user.username,
        first_name=persisted_user.first_name,
        last_name=persisted_user.last_name,
        phone=persisted_user.phone,
        email=persisted_user.email,
        role=persisted_user.role,
    )

    assert user is persisted_user
    assert created is False
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_user_info_commits_only_when_data_changes() -> None:
    session = AsyncMock()
    user = make_user()

    updated = await user_service.update_user_info(
        db=session,
        user=user,
        username="alice_new",
        first_name="Alice",
    )

    assert updated is user
    assert user.username == "alice_new"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_user_info_skips_commit_when_nothing_changed() -> None:
    session = AsyncMock()
    user = make_user()

    updated = await user_service.update_user_info(
        db=session,
        user=user,
        username=user.username,
        first_name=user.first_name,
    )

    assert updated is user
    session.commit.assert_not_awaited()
