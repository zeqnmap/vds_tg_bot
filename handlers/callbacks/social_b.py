from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import (
get_social_submenu_keyboard
)
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()

@router.callback_query(F.data == "social")
async def social_menu_callback(callback: CallbackQuery):
    """Показывает подменю Социализация"""
    text = "Социализация\n\nВыберите интересующий раздел:"
    await callback.message.edit_text(
        text,
        reply_markup=get_social_submenu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "social_about")
async def social_about_callback(callback: CallbackQuery):
    """Текст 'О нас'"""
    about_text = (
        "ЗДРАВПУНКТ\n\n"
        "• Расписание:\n"
        "ПН - ПТ -- 07:00 до 18:00\n"
        "СБ -- 09:00 до 15:00\n"
        "ВС -- Выходной!\n\n"
        "Что сделаем:\n\n"
        "• Оказание первой медицинской помощи в случае травмы или болезни.\n"
        "• Оформление листов о временной нетрудоспособности.\n"
        "• Физиотерапевтические процедуры."
    )
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Социализацию", callback_data="back_to_social")]
    ])
    await callback.message.edit_text(
        about_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "social_contacts")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Контакты'"""
    contacts_text = (
        "📞 В Компании также организованы:\n\n"
        "   • УСЛУГИ МАССАЖА один раз в неделю с возмещением 60% стоимости Компанией\n\n"
        "   • УСЛУГИ ПАРИКМАХЕРА один раз в неделю при самостоятельной оплате\n"

    )
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Социализацию", callback_data="back_to_social")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "social_esg")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Экология'"""
    contacts_text = (
        "ESG - экология, социальной ответственности:\n\n"
        "Важной частью нашей корпоративной философии являются проекты в области ESG — экологии, социальной ответственности и корпоративного управления.\n\n"
        "Мы стремимся быть не только успешной Компанией, но и ответственным участником общества.\n\n"
        "   • Реализована программа эффективного использования природных ресурсов, комплексного управления отходами и переработки.\n\n"
        "   • Компания VDS более 10 лет участвует в сохранении памятников древнерусской живописи и открытии фресок.\n\n"
        "   • Компания VDS разработала и освоила производство высокопроизводительных ульев и современного аналога колоды, и привлекла 8 профессиональных пчеловодов для развития проекта на 12 пасеках в живописнейших уголках Белой Руси. Проект также направлен на возрождение древнего промысла бортничества, включенного в список нематериального культурного наследия ЮНЕСКО."

    )
    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Социализацию", callback_data="back_to_social")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_social")
async def back_to_social_callback(callback: CallbackQuery):
    """Возврат в меню Социализация"""
    await social_menu_callback(callback)

