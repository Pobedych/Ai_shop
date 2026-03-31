from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.models.user import User


async def register_user(
    db: AsyncSession,
    tg_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
    email: str | None,
    phone: str | None,
    role: str | None
) -> User:
    user = User(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        is_active=True,
        role=role,
        balance=0,
        purchase_count=0,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_user(db: AsyncSession, tg_id: int) -> User | None:
    q = select(User).where(User.tg_id == tg_id)
    user = await db.scalar(q)
    return user


async def get_or_create_user(
    db: AsyncSession,
    tg_id: int,
    username: str | None,
    first_name: str | None,
    last_name: str | None,
    phone: str | None,
    email: str | None,
    role: str | None
) -> tuple[User, bool]:
    user = await get_user(db, tg_id)
    if user:
        return user, False
    try:
        user = await register_user(
            db=db,
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role
        )
        await db.commit()
        return user, True
    except IntegrityError:
        await db.rollback()
        user = await get_user(db, tg_id)

        if user is None:
            raise
        return user, False


async def update_user_info(db: AsyncSession, user: User, **kwargs) -> User:
    changed = False
    for key, value in kwargs.items():
        if hasattr(user, key) and getattr(user, key) != value:
            setattr(user, key, value)
            changed = True

    if changed:
        await db.commit()
    return user