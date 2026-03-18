from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import get_usual_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "usual_q")
async def social_menu_callback(callback: CallbackQuery):
    """Показывает подменю Обычные вопросы"""
    text = "❓Вопросы\n\nВыберите интересующий раздел:"
    await callback.message.edit_text(
        text,
        reply_markup=get_usual_submenu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "hygiene")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Гигиена'"""
    contacts_text = (
        "🪥 ЛИЧНАЯ ГИГИЕНА:\n\n"
        "   • В гардеробе предусмотрены персональные шкафчики, душевые, фен.\n\n"
        "   • На территории Завода от проходной до гардероба ЗАПРЕЩЕНО находиться в шортах и в открытой обуви.\n\n"
        "   • Обратите внимание, что в гардеробе отсутствуют полотенце-сушители, предусмотрите для себя каждый день чистое свежее полотенце."
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Вопросы", callback_data="back_to_usual")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "canteen")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Питание'"""
    contacts_text = (
        "🍽️ Питание:\n\n"
        "   • На территории Завода расположена Столовая, где подаются горячие обеды из фермерских продуктов. Оплата проводится по вашему пропуску и расчет производится в конце месяца из суммы ЗП.\n\n"
        "   • Сумма комплексного обеда — 6,50 руб. Компот, горячий чай и хлеб всегда в доступе без ограничений."
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Вопросы", callback_data="back_to_usual")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "salary")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'ЗП'"""
    contacts_text = (
        "💸 ЗАРАБОТНАЯ ПЛАТА:\n\n"
        "Выплачивается 2 раза в месяц:\n\n"
        "АВАНС 10 числа --- ЗП 25 числа\n\n"
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Вопросы", callback_data="back_to_usual")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_usual")
async def back_to_usual_callback(callback: CallbackQuery):
    """Возврат в меню Обычные вопросы"""
    await social_menu_callback(callback)