from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from database.db import Database
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)
router = Router()


class UnusualQuestion(StatesGroup):
    fullname = State()
    phone = State()
    question = State()


@router.callback_query(F.data == "unusual_q")
async def start_unusual(callback: CallbackQuery, state: FSMContext):
    """Начало сценария особого вопроса"""
    await state.set_state(UnusualQuestion.fullname)
    await state.update_data(doc_type="unusual")
    await callback.message.edit_text(
        "⁉️ Задайте ваш особый вопрос.\n\nВведите Ваши ФИО:"
    )
    await callback.answer()


@router.message(UnusualQuestion.fullname)
async def process_fullname(message: Message, state: FSMContext):
    """Получение ФИО, переход к вводу телефона"""
    fullname = message.text.strip()
    await state.update_data(fullname=fullname)
    await state.set_state(UnusualQuestion.phone)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
        ]
    )
    await message.answer(
        "📞 Введите ваш контактный номер телефона (12 цифр, например + 375 (29) 1234567):",
        reply_markup=keyboard,
    )


@router.message(UnusualQuestion.phone)
async def process_phone(message: Message, state: FSMContext):
    """Проверка телефона (12 цифр), переход к вводу вопроса"""
    digits = "".join(filter(str.isdigit, message.text or ""))
    if len(digits) != 12:
        await message.answer("❌ Номер должен содержать 12 цифр. Попробуйте ещё раз:")
        return

    await state.update_data(phone=digits)
    await state.set_state(UnusualQuestion.question)
    await message.answer("📝 Опишите ваш вопрос подробно:")


@router.message(UnusualQuestion.question)
async def process_question(message: Message, state: FSMContext, db: Database):
    """Сохранение вопроса и отправка уведомления"""
    question = message.text.strip()
    await state.update_data(question=question)
    data = await state.get_data()

    await db.save_document_request(
        user_id=message.from_user.id,
        doc_type="unusual",
        fullname=data.get("fullname"),
        phone=data.get("phone"),
        purpose=question,
    )

    await message.answer(
        "✅ Ваш вопрос принят. Мы ответим вам в ближайшее время.\n"
        "Спасибо за обращение!"
    )
    await state.clear()
