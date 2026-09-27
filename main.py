import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from BOT.handlers.start import router as start_router
from BOT.handlers.personality import router as personality_router
from BOT.handlers.astrology import router as astrology_router

from database.database import init_database


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env")


async def main():
    print("🔮 Initializing MYSTRA...")

    # Initialize database
    init_database()

    # Create bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)
    dp.include_router(personality_router)
    dp.include_router(astrology_router)

    print("🔮 MYSTRA Hub is starting...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())