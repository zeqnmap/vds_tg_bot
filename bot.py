import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_PATH
from database.db import Database
from handlers import start_router, main_callback_router  # импортируем оба роутера
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database(DATABASE_PATH)

    # Регистрируем роутеры
    dp.include_router(start_router)  # для /start
    dp.include_router(main_callback_router)  # для всех callback'ов из папки callbacks/

    dp["db"] = db

    await db.create_tables()
    logger.info("Bot started!")

    try:
        await dp.start_polling(bot, db=db)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")