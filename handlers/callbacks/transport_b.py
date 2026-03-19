import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from keyboards.inline import get_transport_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()


@router.callback_query(F.data == "transport")
async def transport_menu_callback(callback: CallbackQuery):
    """Показывает подменю Транспорт"""
    text = "🚎 Транспорт\n\nВыберите интересующий раздел:"
    await callback.message.answer(text, reply_markup=get_transport_submenu_keyboard())
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == "schedule_1")
async def transport_1_contacts_callback(callback: CallbackQuery):
    """Фотография 'Расписание'"""
    photo_path = os.path.join('assets', 'schedule_1.png')

    photo_path = os.path.abspath(photo_path)

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Транспорт", callback_data="back_to_transport")]
    ])
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo=photo,
            caption="🚌 Расписание автобуса",
            reply_markup=back_keyboard
        )
    else:
        await callback.message.answer(
            "Файл с расписанием не найден. Обратитесь к администратору.",
            reply_markup=back_keyboard
        )
    await callback.answer()


@router.callback_query(F.data == "schedule_2")
async def transport_2_contacts_callback(callback: CallbackQuery):
    """Фотография 'Расписание'"""
    photo_path = os.path.join('assets', 'schedule_2.png')

    photo_path = os.path.abspath(photo_path)

    back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="← Назад в Транспорт", callback_data="back_to_transport")]
    ])
    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await callback.message.answer_photo(
            photo=photo,
            caption="🚐 Расписание маршрутки",
            reply_markup=back_keyboard
        )
    else:
        await callback.message.answer(
            "Файл с расписанием не найден. Обратитесь к администратору.",
            reply_markup=back_keyboard
        )
    await callback.answer()


@router.callback_query(F.data == "parking")
async def transport_car_callback(callback: CallbackQuery):
    """Текст 'Парковка'"""
    contacts_text = (
        "🚗 ПАРКОВКА:\n\n"
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
    await transport_menu_callback(callback)