from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.backend.models.user import User

async def register_user(db: AsyncSession, tg_id: int, username: str | None, first_name: str | None, last_name: str| None, email: str | None, phone: str | None) -> User:
    user = User(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        is_active=True,
        role="USER",
        balance=0,
        purchase_count=0
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user(db: AsyncSession, tg_id: int) -> User:
    q = select(User).where(User.tg_id == tg_id)
    user = await db.scalar(q)
    return user

async def get_or_create_user(
db: AsyncSession, tg_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
        phone: str | None,
        email: str | None,
) -> tuple[User, bool]:
    q = select(User).where(User.tg_id == tg_id)
    user = await db.scalar(q)
    if user:
        return user, False

    user = await register_user(
        db=db,
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
    )
    return user, True


