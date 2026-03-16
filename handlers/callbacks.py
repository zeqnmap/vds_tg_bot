from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from keyboards.inline import (
    get_main_menu_keyboard,
    get_back_button,
    get_settings_keyboard,
    get_contacts_keyboard,
get_social_submenu_keyboard
)
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()

# ========== ОСНОВНЫЕ РАЗДЕЛЫ ==========



@router.callback_query(F.data == "study")
async def info_callback(callback: CallbackQuery):
    """Информация о боте"""
    info_text = (
        "ℹ️ **Информация о боте**\n\n"
        "• **Версия:** 1.0.0\n"
        "• **Библиотека:** aiogram 3.x\n"
        "• **База данных:** SQLite\n"
        "• **Тип кнопок:** Inline (внутри сообщения)\n"
        "• **Кнопки:** 5 основных + подменю"
    )
    await callback.message.edit_text(
        info_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "transport")
async def stats_callback(callback: CallbackQuery, db: Database):
    """Статистика бота"""
    users = await db.get_all_users()
    user_count = len(users)
    stats_text = (
        f"📊 **Статистика бота**\n\n"
        f"• **Всего пользователей:** {user_count}\n"
        f"• **Активных сегодня:** {user_count} (демо)\n"
        f"• **Всего команд:** несколько inline-кнопок"
    )
    await callback.message.edit_text(
        stats_text,
        reply_markup=get_back_button(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "usual_q")
async def settings_callback(callback: CallbackQuery):
    """Меню настроек"""
    settings_text = "⚙️ **Настройки**\n\nВыберите категорию:"
    await callback.message.edit_text(
        settings_text,
        reply_markup=get_settings_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@router.callback_query(F.data == "unusual_q")
async def contacts_callback(callback: CallbackQuery):
    """Контакты со ссылками"""
    contacts_text = "📞 **Контакты**\n\nНажмите на ссылки ниже, чтобы перейти:"
    await callback.message.edit_text(
        contacts_text,
        reply_markup=get_contacts_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()








# ========== ОБРАБОТКА ВСЕХ ОСТАЛЬНЫХ СООБЩЕНИЙ ==========

@router.message()
async def handle_unknown(message):
    """Обработка ошибочный сообщений"""
    await message.answer(
        "Я понимаю только команду /start и кнопки.\n"
        "Нажмите /start для начала работы.",
        reply_markup=get_main_menu_keyboard()
    )