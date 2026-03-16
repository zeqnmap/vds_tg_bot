from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import get_transport_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "transport")
async def social_menu_callback(callback: CallbackQuery):
    """Показывает подменю Транспорт"""
    text = "Обучение\n\nВыберите интересующий раздел:"
    await callback.message.edit_text(
        text,
        reply_markup=get_transport_submenu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "schedule")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Расписание'"""
    contacts_text = (
        "📞 РАСПИСАНИЕ АВТОБУСОВ:\n\n"
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Транспорт", callback_data="back_to_transport")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "parking")
async def social_contacts_callback(callback: CallbackQuery):
    """Текст 'Парковка'"""
    contacts_text = (
        "📞 ПАРКОВКА:\n\n"
        "Парковаться можно вдоль дороги или на горизонтальной парковке перед входом в офис рядом с проходной.\n\n"
        "   • В случае если вы перекрыли выезд другому припаркованному автомобилю, обязательно оставьте под стеклом свой контактный номер телефона.\n\n"
        "   • Места на парковке под шлагбаумом и на вертикальной парковке у входа в офиса закреплены за действующими сотрудниками и по мере возможности будут перераспределятся."
    )

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Транспорт", callback_data="back_to_transport")]
    ])
    await callback.message.edit_text(
        contacts_text,
        reply_markup=back_keyboard
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_transport")
async def back_to_transport_callback(callback: CallbackQuery):
    """Возврат в меню Транспорт"""
    await social_menu_callback(callback)