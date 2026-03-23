from aiogram import F, Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "study")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст Платформа"""
    contacts_text = (
        "💻 В Компании есть платформа дистанционного обучения:\n\n"
        "   • Логин и пароль от вашего личного кабинета на платформу вам выдаст HR специалист.\n"
        "   • В первый день назначаются курсы, которые понадобятся вам в процессе работы.\n"
        "   • ВАЖНО пройти их в течение первого месяца работы‼️\n\n"
        "Дополнительно:\n"
        "   • Доступен каталог курсов по профессиям, навыкам\n"
        "   • Есть библиотека с книгами\n\n"
        "📱 Как зайти:\n"
        "   • Через браузер: vds.ispring.ru\n"
        "   • Через приложение iSpring Learn\n\n"
        "Также можно скачать приложение:\n\n"
        "iPhone: https://apps.apple.com/kz/app/ispring-lms/id836648214\n\n"
        "Android: https://play.google.com/store/apps/details?id=com.ispring.islearn"
    )

    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="← Назад", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(contacts_text, reply_markup=back_keyboard)
    await callback.answer()
