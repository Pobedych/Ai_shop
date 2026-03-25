from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from app.backend.models.item import Item


async def new_item(
        db: AsyncSession,
        name: str,
        description: str,
        mini_description: str,
        category: str,
        price: Decimal,
        count: int,
) -> Item:
    item = Item(
        name=name,
        description=description,
        mini_description=mini_description,
        category=category,
        price=price,
        count=count,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item

async def get_item_by_category(db: AsyncSession, category: str) -> list[Item]:
    q = select(Item).where(Item.category == category)
    result = await db.scalars(q)
    return list(result.all())


async def get_all_categories(db: AsyncSession) -> list[str]:
    query = select(Item.category).distinct().order_by(Item.category)
    result = await db.scalars(query)
    return list(result.all())

