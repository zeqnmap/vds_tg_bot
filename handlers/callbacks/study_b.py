from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import get_study_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "study")
async def social_menu_callback(callback: CallbackQuery):
    """Показывает подменю Обучения"""
    text = "📚Обучение\n\nВыберите интересующий раздел:"
    await callback.message.edit_text(
        text,
        reply_markup=get_study_submenu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "platform")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Платформа'"""
    contacts_text = (
        "💻 В Компании есть платформа дистанционного обучения:\n\n"
        "   • Логин и пароль от вашего личного кабинета на платформу вам выдаст HR специалист.\n\n"
        "   • В первый день назначаются курсы, которые понадобятся вам в процессе работы.\n\n"
        "   • ВАЖНО пройти их в течение первого месяца работы!!!\n\n"
        "   • Вам также доступен КАТАЛОГ курсов по вашим интересам\n\n"
        "ПРИЛОЖЕНИЕ ДЛЯ ОБУЧЕНИЯ:\n\n"
        "   • Скачивай приложение iSpring Learn на телефон или заходи по ссылке в браузере: vds.ispring.ru:\n\n"
        "Для iPhone: https://apps.apple.com/kz/app/ispring-lms/id836648214\n\n"
        "Для Android: https://play.google.com/store/apps/details?id=com.ispring.islearn"
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Обучение", callback_data="back_to_study")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "church")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Церковь'"""
    contacts_text = (
        "⛪️ ДУХОВНЫЙ ИНТЕЛЛЕКТ:\n\n"
        "На территории Завода есть Часовня Святителя Спиридона Тримифунтского.\n"
        "Здесь у каждого из нас есть возможность получить духовную поддержку, найти умиротворение и вдохновение.\n\n"
        "Каждый ЧЕТВЕРГ в 07:00 проходит Литургия.\n"
        "Приглашаем!!!"
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Обучение", callback_data="back_to_study")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_study")
async def back_to_study_callback(callback: CallbackQuery):
    """Возврат в меню Обучение"""
    await social_menu_callback(callback)