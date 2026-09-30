import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from BOT.handlers.start import router as start_router
from BOT.handlers.personality import router as personality_router
from BOT.handlers.astrology import router as astrology_router
from BOT.handlers.results import router as results_router

from database.database import init_database


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")


class MYSTRAAiohttpSession(AiohttpSession):
    def __init__(self, proxy: str):
        super().__init__(proxy=proxy)

        # Disable SSL certificate verification for the local SOCKS5 proxy.
        # The local proxy uses its own certificate.
        self._connector_init["ssl"] = False


async def main():
    print("🔮 Initializing MYSTRA...")

    # Initialize database
    init_database()

    # Get proxy from environment
    proxy_url = os.getenv("PROXY_URL")

    if not proxy_url:
        raise ValueError("PROXY_URL is not set in .env")

    # Create custom aiogram session using the local SOCKS5 proxy
    session = MYSTRAAiohttpSession(proxy=proxy_url)

    # Create bot
    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # Create dispatcher
    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)
    dp.include_router(personality_router)
    dp.include_router(astrology_router)
    dp.include_router(results_router)

    print("🔮 MYSTRA Hub is starting...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())