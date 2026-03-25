from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from app.backend.core.database import SessionLocal
from app.backend.services.shop_service import get_all_categories, get_item_by_category
from app.bot.keyboards.inlinekey import categories_menu, items_menu

shop_router = Router()


@shop_router.callback_query(F.data == "shop")
async def shop(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()

    async with SessionLocal() as session:
        categories = await get_all_categories(session)

    await cq.message.answer(
        i18n.get("shop-choose-category"),
        reply_markup=categories_menu(categories),
    )


@shop_router.callback_query(F.data.startswith("category:"))
async def category_items(cq: CallbackQuery, i18n: I18nContext):
    await cq.answer()
    category = cq.data.split(":", maxsplit=1)[1]

    async with SessionLocal() as session:
        items = await get_item_by_category(session, category)

    if not items:
        await cq.message.answer(i18n.get("shop-empty-category", category=category))
        return

    await cq.message.answer(
        i18n.get("shop-choose-item", category=category),
        reply_markup=items_menu(items),
    )
