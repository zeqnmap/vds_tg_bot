from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.db import Database
from keyboards.inline import get_main_menu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: Database):
    """Обработчик /start – сохраняет пользователя и показывает inline-меню"""
    user_id = message.from_user.id
    username = message.from_user.username

    await db.add_user(user_id, username)

    welcome_text = (
        f"👋 Привет, {message.from_user.full_name}!\n\n"
        f"Я бот для новых работников и гостей Компании!\n"
        f"Выбирайте интересующую тему и узнавайте о ней!"
    )

    await message.answer(
        welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown"
    )
    logger.info(f"User {user_id} started the bot")
