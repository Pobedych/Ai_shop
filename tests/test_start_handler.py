from unittest.mock import AsyncMock

import pytest

from app.backend.models.user import User
from app.bot.handlers.start import money


class DummyI18n:
    def get(self, key: str, **kwargs) -> str:
        if kwargs:
            return f"{key}:{kwargs}"
        return key


def make_user(balance: int = 0) -> User:
    return User(
        tg_id=123456,
        username="alice",
        first_name="Alice",
        last_name="Doe",
        email=None,
        phone=None,
        role="USER",
        balance=balance,
        purchase_count=0,
    )


@pytest.mark.asyncio
async def test_money_rejects_non_numeric_amount() -> None:
    message = AsyncMock()
    message.text = "abc"
    state = AsyncMock()
    session = AsyncMock()
    db_user = make_user(balance=10)

    await money(
        message=message,
        i18n=DummyI18n(),
        state=state,
        db_user=db_user,
        session=session,
    )

    assert db_user.balance == 10
    session.commit.assert_not_awaited()
    state.clear.assert_not_awaited()
    message.answer.assert_awaited_once_with("top-up-invalid-amount")


@pytest.mark.asyncio
async def test_money_rejects_non_positive_amount() -> None:
    message = AsyncMock()
    message.text = "0"
    state = AsyncMock()
    session = AsyncMock()
    db_user = make_user(balance=10)

    await money(
        message=message,
        i18n=DummyI18n(),
        state=state,
        db_user=db_user,
        session=session,
    )

    assert db_user.balance == 10
    session.commit.assert_not_awaited()
    state.clear.assert_not_awaited()
    message.answer.assert_awaited_once_with("top-up-amount-positive")


@pytest.mark.asyncio
async def test_money_updates_balance_and_clears_state_on_success() -> None:
    message = AsyncMock()
    message.text = "25"
    state = AsyncMock()
    session = AsyncMock()
    db_user = make_user(balance=10)

    await money(
        message=message,
        i18n=DummyI18n(),
        state=state,
        db_user=db_user,
        session=session,
    )

    assert db_user.balance == 35
    session.commit.assert_awaited_once()
    state.clear.assert_awaited_once()
    message.answer.assert_awaited_once_with("top-up-success:{'balance': 35}")
