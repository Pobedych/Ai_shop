import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores.fluent_compile_core import FluentCompileCore

from app.bot.create_bot import bot, dp
from app.bot.handlers.shop import shop_router
from app.bot.handlers.start import router


async def main():
    dp.include_router(router)
    dp.include_router(shop_router)
    locales_path = (
        Path(__file__).resolve().parent / "locales" / "{locale}" / "LC_MESSAGES"
    ).as_posix()
    i18n_middleware = I18nMiddleware(
        core=FluentCompileCore(path=locales_path, default_locale="en")
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
