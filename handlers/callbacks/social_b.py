from aiogram import F, Router
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)

from keyboards.inline import get_social_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "social")
async def social_menu_callback(callback: CallbackQuery):
    """Показывает подменю Социализация"""
    text = "👷Социализация\n\nВыберите интересующий раздел:"
    await callback.message.edit_text(text, reply_markup=get_social_submenu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "social_about")
async def social_about_callback(callback: CallbackQuery):
    """Текст 'О нас'"""
    about_text = (
        "🏥 ЗДРАВПУНКТ\n\n"
        "• Расписание:\n"
        "ПН - ПТ -- 07:00 до 18:00\n"
        "СБ -- 09:00 до 15:00\n"
        "ВС -- Выходной!\n\n"
        "Дежурный телефон: +375 (29) 6907746\n"
        "Пн-Пт: 7:00-22:00, Сб-Вс: 9:00-22:00\n"
        "—————————————————————\n"
        "Услуги:\n\n"
        "   • Оказание первой медицинской помощи в случае травмы или болезни.\n"
        "   • Оформление больничного листа.\n"
        "   • Выполнение процедур (инъекции, капельницы, забор анализов, медицинские исследования)\n"
        "   • Выездные консультации\n"
        "   • Физиотерапевтические процедуры\n"
        "   • Массаж"
    )
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Социализацию", callback_data="back_to_social"
                )
            ]
        ]
    )
    await callback.message.edit_text(about_text, reply_markup=back_keyboard)
    await callback.answer()


@router.callback_query(F.data == "social_contacts")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Контакты'"""
    contacts_text = (
        "🙏 В Компании также организованы:\n\n"
        "   • УСЛУГИ МАССАЖА один раз в неделю с возмещением 60% стоимости Компанией\n"
        "Записаться вы можете через нашего администратора:\n\n"
        "Лапун Полина - +375 (29) 6442312\n\n"
        "   • УСЛУГИ ПАРИКМАХЕРА один раз в неделю при самостоятельной оплате\n"
    )
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Социализацию", callback_data="back_to_social"
                )
            ]
        ]
    )
    await callback.message.edit_text(
        contacts_text, reply_markup=back_keyboard, parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "social_esg")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Экология'"""
    contacts_text = (
        "🌳 ЭКОЛОГИЯ\n\n"
        "Мы развиваем инициативы в области экологии, социальной ответственности и устойчивого развития — это важная часть жизни Компании VDS.\n\n"
        "• Мы бережно относимся к ресурсам: сортируем и перерабатываем отходы — на территории VDS работает более 10 пунктов сбора.\n\n"
        "• Мы сохраняем культурное наследие: уже более 10 лет участвуем в проектах по восстановлению древнерусской живописи.\n\n"
        "• Мы возрождаем традиции: развиваем пчеловодство и бортничество, работаем с 8 профессиональными пчеловодами на 12 пасеках по всей Беларуси и ежегодно вместе с Командой участвуем в сборе меда.\n\n"
        "• Мы заботимся о природе: подкармливаем малых птиц и поддерживаем их популяцию. Кормушки можно найти по всей территории Завода.\n\n"
        "• Мы создаем зеленую среду: вместе высаживаем деревья и развиваем ландшафтный парк — вместе мы высадили более 60 000 деревьев!\n\n"
        "К этим проектам можно присоединиться — следите за анонсами и участвуйте вместе с Командой 🌱"
    )
    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Социализацию", callback_data="back_to_social"
                )
            ]
        ]
    )
    await callback.message.edit_text(
        contacts_text, reply_markup=back_keyboard, parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "church")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст Церковь"""
    contacts_text = (
        " ⛪️ ДУХОВНЫЙ ИНТЕЛЛЕКТ:\n\n"
        "На территории Завода находится часовня Святителя Спиридона Тримифунтского.\n\n"
        "Здесь у каждого из нас есть возможность найти духовную поддержку, найти умиротворение и вдохновение.\n\n"
        "🕖 Каждый четверг в 07:00 проходит Литургия\n\n"
        "🕐 Каждую пятницу в 13:00 проходит молебен Святителя Спиридона Тримифунтского\n\n"
        "Будем рады видеть вас!\n\n"
        "🔗 Телеграм-канал: @hramgor"
    )

    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Обучение", callback_data="back_to_social"
                )
            ]
        ]
    )
    await callback.message.edit_text(contacts_text, reply_markup=back_keyboard)
    await callback.answer()


@router.callback_query(F.data == "back_to_social")
async def back_to_social_callback(callback: CallbackQuery):
    """Возврат в меню Социализация"""
    await social_menu_callback(callback)
