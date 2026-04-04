import asyncio
from pathlib import Path

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from app.bot.create_bot import bot, dp
from app.bot.handlers.shop import shop_router
from app.bot.handlers.start import router
from app.bot.handlers.admins_only import admin_router
from app.bot.middleware.user import UserMiddleware
from app.bot.middleware.db import DbSessionMiddleware
from app.bot.middleware.i18n_manager import UserManager


async def main():
    # Регистрация роутеров
    dp.include_router(shop_router)
    dp.include_router(admin_router)
    dp.include_router(router)
    # 1. Открываем сессию БД
    dp.update.outer_middleware(DbSessionMiddleware())
    # 2. Достаем юзера из БД (берет сессию из данных)
    dp.update.outer_middleware(UserMiddleware())

    locales_path = (
        Path(__file__).resolve().parent / "locales" / "{locale}" / "LC_MESSAGES"
    ).as_posix()

    # 3. Настраиваем локализацию (берет юзера из данных)
    i18n_middleware = I18nMiddleware(
        core=FluentCompileCore(path=locales_path, default_locale="en"),
        manager=UserManager(),
    )
    i18n_middleware.setup(dispatcher=dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
