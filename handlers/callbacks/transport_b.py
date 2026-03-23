import os

from aiogram import F, Router
from aiogram.types import (CallbackQuery, FSInputFile, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaPhoto)

from keyboards.inline import get_transport_submenu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()

sent_messages = {}


@router.callback_query(F.data == "transport")
async def transport_menu_callback(callback: CallbackQuery):
    """Показывает подменю Транспорт"""
    text = (
        "🚎 Транспорт\n\n"
        "В Компании организована доставка сотрудников по двум направлениям:\n\n"
        "1) Игуменский тракт - ст.м. «Институт культуры» - ст.м. «Пушкинская» - ст.м. «Каменная горка»\n"
        "2) ст.м. «Малиновка»\n\n"
        "Выберите интересующий раздел:"
    )

    await callback.message.answer(text, reply_markup=get_transport_submenu_keyboard())
    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == "schedule_1")
async def schedule_callback(callback: CallbackQuery):
    image_files = [
        "schedule_1.png",
        "schedule_2.png",
        "schedule_3.png",
    ]  # замените на свои имена
    photos = []
    for f_name in image_files:
        file_path = os.path.abspath(os.path.join("assets", f_name))
        if os.path.exists(file_path):
            photos.append(InputMediaPhoto(media=FSInputFile(file_path)))
        else:
            logger.warning(f"Файл не найден: {file_path}")

    if not photos:
        back_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="← Назад в Транспорт", callback_data="back_to_transport"
                    )
                ]
            ]
        )
        await callback.message.answer(
            "Файлы с расписанием не найдены. Обратитесь к администратору.",
            reply_markup=back_keyboard,
        )
        await callback.answer()
        return

    sent_msgs = await callback.message.answer_media_group(media=photos)
    msg_ids = [msg.message_id for msg in sent_msgs]

    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Транспорт", callback_data="back_to_transport"
                )
            ]
        ]
    )
    back_msg = await callback.message.answer(
        "🚌 Расписание автобуса", reply_markup=back_keyboard
    )
    msg_ids.append(back_msg.message_id)

    msg_ids.append(callback.message.message_id)

    user_id = callback.from_user.id
    sent_messages[user_id] = msg_ids

    await callback.answer()


@router.callback_query(F.data == "schedule_2")
async def schedule_callback(callback: CallbackQuery):
    image_files = ["schedule_4.png", "schedule_5.png"]
    photos = []
    for f_name in image_files:
        file_path = os.path.abspath(os.path.join("assets", f_name))
        if os.path.exists(file_path):
            photos.append(InputMediaPhoto(media=FSInputFile(file_path)))
        else:
            logger.warning(f"Файл не найден: {file_path}")

    if not photos:
        back_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="← Назад в Транспорт", callback_data="back_to_transport"
                    )
                ]
            ]
        )
        await callback.message.answer(
            "Файлы с расписанием не найдены. Обратитесь к администратору.",
            reply_markup=back_keyboard,
        )
        await callback.answer()
        return

    sent_msgs = await callback.message.answer_media_group(media=photos)
    msg_ids = [msg.message_id for msg in sent_msgs]

    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Транспорт", callback_data="back_to_transport"
                )
            ]
        ]
    )
    back_msg = await callback.message.answer(
        "🚐 Расписание маршрутки", reply_markup=back_keyboard
    )
    msg_ids.append(back_msg.message_id)

    msg_ids.append(callback.message.message_id)

    user_id = callback.from_user.id
    sent_messages[user_id] = msg_ids

    await callback.answer()


@router.callback_query(F.data == "parking")
async def transport_car_callback(callback: CallbackQuery):
    """Текст 'Парковка'"""
    contacts_text = (
        "🚗 ПАРКОВКА:\n\n"
        "Парковаться можно вдоль дороги или на горизонтальной парковке перед входом в офис рядом с проходной.\n\n"
        "   • В случае если вы перекрыли выезд другому припаркованному автомобилю, обязательно оставьте под стеклом свой контактный номер телефона.\n\n"
        "   • Места на парковке под шлагбаумом и на вертикальной парковке у входа в офиса закреплены за действующими сотрудниками и по мере возможности будут перераспределятся.\n\n"
        "🚲 Парковка для велосипедов находится возле проходной завода"
    )

    back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="← Назад в Транспорт", callback_data="back_to_transport_park"
                )
            ]
        ]
    )
    await callback.message.edit_text(contacts_text, reply_markup=back_keyboard)
    await callback.answer()


@router.callback_query(F.data == "back_to_transport_park")
async def back_to_transport_callback(callback: CallbackQuery):
    """Возврат в меню Транспорт для парковки"""
    await transport_menu_callback(callback)


@router.callback_query(F.data == "back_to_transport")
async def back_to_transport_callback(callback: CallbackQuery):
    user_id = callback.from_user.id

    # удаляем все сообщения, связанные с расписанием
    if user_id in sent_messages:
        for msg_id in sent_messages[user_id]:
            try:
                await callback.bot.delete_message(
                    chat_id=callback.message.chat.id, message_id=msg_id
                )
            except Exception as e:
                logger.error(f"Не удалось удалить сообщение {msg_id}: {e}")
        del sent_messages[user_id]

    text = (
        "🚎 Транспорт\n\n"
        "В Компании организована доставка сотрудников по двум направлениям:\n\n"
        "1) Игуменский тракт - ст.м. «Институт культуры» - ст.м. «Пушкинская» - ст.м. «Каменная горка»\n"
        "2) ст.м. «Малиновка»\n\n"
        "Выберите интересующий раздел:"
    )
    await callback.message.answer(text, reply_markup=get_transport_submenu_keyboard())
    await callback.answer()
