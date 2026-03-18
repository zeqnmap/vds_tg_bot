import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_PATH, NOTIFICATION_CHAT_ID, NOTIFICATION_INTERVAL
from database.db import Database
from handlers import start_router, main_callback_router
from services.notifier import monitor_new_requests
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    db = Database(DATABASE_PATH)

    dp.include_router(start_router)
    dp.include_router(main_callback_router)

    dp["db"] = db

    await db.create_tables()
    logger.info("Bot started!")

    if NOTIFICATION_CHAT_ID:
        asyncio.create_task(
            monitor_new_requests(bot, db, NOTIFICATION_CHAT_ID, NOTIFICATION_INTERVAL)
        )
        logger.info(f"Запущен мониторинг новых заявок для чата {NOTIFICATION_CHAT_ID}")
    else:
        logger.info("Уведомления о новых заявках отключены (не задан NOTIFICATION_CHAT_ID)")

    try:
        await dp.start_polling(bot, db=db)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")