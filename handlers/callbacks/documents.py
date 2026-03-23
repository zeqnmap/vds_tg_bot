import os

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message)

from config import UPLOADS_DIR
from database.db import Database
from keyboards.inline import get_doc_menu_keyboard
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)
router = Router()

# ========== FSM СОСТОЯНИЯ ДЛЯ КАЖДОГО ТИПА ДОКУМЕНТА ==========


class SalaryDoc(StatesGroup):
    """Справка о заработной плате (пункт 1)"""

    fullname = State()
    phone = State()  # добавлено поле для телефона
    purpose = State()
    period = State()
    organization = State()
    form = State()


class PeriodDoc(StatesGroup):
    """Справка о периоде, месте работы и должности (пункт 2)"""

    fullname = State()
    phone = State()
    purpose = State()
    organization = State()
    form = State()


class CopyDoc(StatesGroup):
    """Копия трудовой книжки (пункт 3)"""

    fullname = State()
    phone = State()
    copy_type = State()  # ксерокопия / заверенная
    organization = State()


class VacationDoc(StatesGroup):
    """Справка о периоде отпуска (пункт 4)"""

    fullname = State()
    phone = State()
    vacation_type = State()  # трудовой/социальный или по уходу за ребенком
    purpose = State()
    organization = State()
    form = State()


class ChildDoc(StatesGroup):
    """Справка о необеспеченности ребенка путевкой (пункт 5)"""

    fullname = State()  # ФИО родителя
    phone = State()
    child_fullname = State()
    child_birth = State()
    certificate_type = State()  # оздоровительный лагерь / санаторное лечение
    organization = State()
    # без формы


class ReferenceDoc(StatesGroup):
    """Характеристика (пункт 6)"""

    fullname = State()
    phone = State()
    ref_type = State()  # производственная / произвольная
    organization = State()
    form = State()


class PetitionDoc(StatesGroup):
    """Ходатайство (пункт 7)"""

    fullname = State()
    phone = State()
    petition_topic = State()  # о чем ходатайствовать
    organization = State()
    form = State()


class OtherDoc(StatesGroup):
    """Другой документ (пункт 8)"""

    fullname = State()
    phone = State()
    doc_name = State()  # какой документ
    organization = State()
    form = State()


# ========== ВХОД В МЕНЮ ДОКУМЕНТОВ ==========


@router.callback_query(F.data == "doc_menu")
async def show_doc_menu(callback: CallbackQuery):
    text = (
        "📋 Пожалуйста, выберите документ, который Вам необходим:\n\n"
        "1️⃣ Справка о заработной плате\n\n"
        "2️⃣ Справка о периоде, месте работы и занимаемой должности\n\n"
        "3️⃣ Копия трудовой книжки\n\n"
        "4️⃣ Справка о периоде отпуска\n\n"
        "5️⃣ Справка о необеспеченности ребенка путевкой\n\n"
        "6️⃣ Характеристика\n\n"
        "7️⃣ Ходатайство\n\n"
        "8️⃣ Другой документ\n\n"
    )
    await callback.message.edit_text(text, reply_markup=get_doc_menu_keyboard())
    await callback.answer()


# ========== ОБРАБОТЧИКИ ЗАПУСКА ДЛЯ КАЖДОГО ПУНКТА ==========


@router.callback_query(F.data == "doc_salary")
async def start_salary(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SalaryDoc.fullname)
    await state.update_data(doc_type="salary")
    await callback.message.edit_text(
        "📝 Для оформления справки о заработной плате введите Ваши ФИО:"
    )
    await callback.answer()


@router.callback_query(F.data == "doc_period")
async def start_period(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PeriodDoc.fullname)
    await state.update_data(doc_type="period")
    await callback.message.edit_text(
        "📝 Для справки о периоде, месте работы и занимаемой должности введите Ваши ФИО:"
    )
    await callback.answer()


@router.callback_query(F.data == "doc_copy")
async def start_copy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CopyDoc.fullname)
    await state.update_data(doc_type="copy")
    await callback.message.edit_text(
        "📝 Для получения копии трудовой книжки введите Ваши ФИО:"
    )
    await callback.answer()


@router.callback_query(F.data == "doc_vacation")
async def start_vacation(callback: CallbackQuery, state: FSMContext):
    await state.set_state(VacationDoc.fullname)
    await state.update_data(doc_type="vacation")
    await callback.message.edit_text(
        "📝 Для справки о периоде отпуска введите Ваши ФИО:"
    )
    await callback.answer()


@router.callback_query(F.data == "doc_child")
async def start_child(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChildDoc.fullname)
    await state.update_data(doc_type="child")
    await callback.message.edit_text(
        "📝 Для справки о необеспеченности ребенка путевкой введите Ваши ФИО (заявителя):"
    )
    await callback.answer()


@router.callback_query(F.data == "doc_reference")
async def start_reference(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReferenceDoc.fullname)
    await state.update_data(doc_type="reference")
    await callback.message.edit_text("📝 Для характеристики введите Ваши ФИО:")
    await callback.answer()


@router.callback_query(F.data == "doc_petition")
async def start_petition(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PetitionDoc.fullname)
    await state.update_data(doc_type="petition")
    await callback.message.edit_text("📝 Для ходатайства введите Ваши ФИО:")
    await callback.answer()


@router.callback_query(F.data == "doc_other")
async def start_other(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OtherDoc.fullname)
    await state.update_data(doc_type="other")
    await callback.message.edit_text("📝 Для другого документа введите Ваши ФИО:")
    await callback.answer()


# ========== ОБЩИЙ ОБРАБОТЧИК ВВОДА ФИО ==========
# после получения ФИО перевод на ввод телефона


@router.message(SalaryDoc.fullname)
@router.message(PeriodDoc.fullname)
@router.message(CopyDoc.fullname)
@router.message(VacationDoc.fullname)
@router.message(ChildDoc.fullname)
@router.message(ReferenceDoc.fullname)
@router.message(PetitionDoc.fullname)
@router.message(OtherDoc.fullname)
async def process_fullname(message: Message, state: FSMContext):
    fullname = message.text.strip()
    await state.update_data(fullname=fullname)
    data = await state.get_data()
    doc_type = data.get("doc_type")

    # переход к вводу телефона в зависимости от типа документа
    if doc_type == "salary":
        await state.set_state(SalaryDoc.phone)
    elif doc_type == "period":
        await state.set_state(PeriodDoc.phone)
    elif doc_type == "copy":
        await state.set_state(CopyDoc.phone)
    elif doc_type == "vacation":
        await state.set_state(VacationDoc.phone)
    elif doc_type == "child":
        await state.set_state(ChildDoc.phone)
    elif doc_type == "reference":
        await state.set_state(ReferenceDoc.phone)
    elif doc_type == "petition":
        await state.set_state(PetitionDoc.phone)
    elif doc_type == "other":
        await state.set_state(OtherDoc.phone)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_doc_menu")]
        ]
    )
    await message.answer(
        "📞 Введите ваш контактный номер телефона (12 цифр, например + 375 (29) 1234567):",
        reply_markup=keyboard,
    )


# ========== ОБРАБОТЧИК ВВОДА ТЕЛЕФОНА ==========
# проверка, что номер содержит 12 цифр, затем переход к следующему шагу


@router.message(SalaryDoc.phone)
@router.message(PeriodDoc.phone)
@router.message(CopyDoc.phone)
@router.message(VacationDoc.phone)
@router.message(ChildDoc.phone)
@router.message(ReferenceDoc.phone)
@router.message(PetitionDoc.phone)
@router.message(OtherDoc.phone)
async def process_phone(message: Message, state: FSMContext):
    digits = "".join(filter(str.isdigit, message.text))
    if len(digits) != 12:
        await message.answer(
            "❌ Номер должен содержать 12 цифр (например, + 375 (29) 1234567). Попробуйте ещё раз:"
        )
        return

    await state.update_data(phone=digits)
    data = await state.get_data()
    doc_type = data.get("doc_type")

    if doc_type == "salary":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏠 Кредит на жильё", callback_data="purpose_house"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚗 Кредит на машину", callback_data="purpose_car"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🏡 Улучшение жилищных условий",
                        callback_data="purpose_improve",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📄 Налоговая", callback_data="purpose_tax"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🛒 Потребительский кредит",
                        callback_data="purpose_consumer",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📦 Рассрочка на товары",
                        callback_data="purpose_installment",
                    )
                ],
                [InlineKeyboardButton(text="✏️ Другое", callback_data="purpose_other")],
                [
                    InlineKeyboardButton(
                        text="🔙 Назад в меню документов",
                        callback_data="back_to_doc_menu",
                    )
                ],
            ]
        )
        await message.answer("Выберите цель получения справки:", reply_markup=keyboard)
        await state.set_state(SalaryDoc.purpose)

    elif doc_type == "period":
        await message.answer("Укажите, для чего нужна справка:")
        await state.set_state(PeriodDoc.purpose)

    elif doc_type == "copy":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📄 Достаточно ксерокопии", callback_data="copy_simple"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📜 Заверенная подписью и печатью",
                        callback_data="copy_certified",
                    )
                ],
            ]
        )
        await message.answer("Выберите, какая копия нужна:", reply_markup=keyboard)
        await state.set_state(CopyDoc.copy_type)

    elif doc_type == "vacation":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏖 Трудовой или социальный отпуск",
                        callback_data="vacation_regular",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👶 Отпуск по уходу за ребенком",
                        callback_data="vacation_childcare",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Назад в меню документов",
                        callback_data="back_to_doc_menu",
                    )
                ],
            ]
        )
        await message.answer("Выберите, какая справка нужна:", reply_markup=keyboard)
        await state.set_state(VacationDoc.vacation_type)

    elif doc_type == "child":
        await message.answer("Введите ФИО ребенка:")
        await state.set_state(ChildDoc.child_fullname)

    elif doc_type == "reference":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🏭 Производственная характеристика",
                        callback_data="ref_production",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📄 В произвольной форме", callback_data="ref_arbitrary"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Назад в меню документов",
                        callback_data="back_to_doc_menu",
                    )
                ],
            ]
        )
        await message.answer(
            "Выберите, какая характеристика нужна:", reply_markup=keyboard
        )
        await state.set_state(ReferenceDoc.ref_type)

    elif doc_type == "petition":
        await message.answer("О чем должна ходатайствовать Компания? (укажите):")
        await state.set_state(PetitionDoc.petition_topic)

    elif doc_type == "other":
        await message.answer("Какой документ Вам необходимо получить? (укажите):")
        await state.set_state(OtherDoc.doc_name)


# ========== ВОЗВРАТ В МЕНЮ ДОКУМЕНТОВ ==========


@router.callback_query(F.data == "back_to_doc_menu")
async def back_to_doc_menu_callback(callback: CallbackQuery, state: FSMContext):
    """Вернуться назад в меню документов и сбросить состояние"""
    await state.clear()
    await show_doc_menu(callback)


# ========== ОБРАБОТЧИКИ ДЛЯ СПРАВКИ О ЗАРПЛАТЕ (salary) ==========


@router.callback_query(SalaryDoc.purpose)
async def salary_purpose(callback: CallbackQuery, state: FSMContext):
    purpose = callback.data.replace("purpose_", "")
    await state.update_data(purpose=purpose)

    if purpose in ("consumer", "installment"):
        await callback.message.edit_text(
            "❌ СПРАВКА О ЗАРАБОТНОЙ ПЛАТЕ НЕ МОЖЕТ БЫТЬ ВЫДАНА для данной цели.\n"
            "Вернитесь в меню документов и выберите другой документ.",
            reply_markup=get_doc_menu_keyboard(),
        )
        await state.clear()
        await callback.answer()
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="3 месяца", callback_data="period_3")],
            [InlineKeyboardButton(text="6 месяцев", callback_data="period_6")],
            [InlineKeyboardButton(text="12 месяцев", callback_data="period_12")],
            [InlineKeyboardButton(text="Иной период", callback_data="period_other")],
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню документов", callback_data="back_to_doc_menu"
                )
            ],
        ]
    )
    await callback.message.edit_text(
        "Выберите период, за который нужна справка:", reply_markup=keyboard
    )
    await state.set_state(SalaryDoc.period)
    await callback.answer()


@router.callback_query(SalaryDoc.period)
async def salary_period(callback: CallbackQuery, state: FSMContext):
    period = callback.data.replace("period_", "")
    await state.update_data(period=period)

    if period == "other":
        await callback.message.edit_text(
            "Укажите нужный период вручную (например, 'с 01.01.2024 по 01.06.2024'):"
        )
        await state.set_state(SalaryDoc.organization)
    else:
        await callback.message.edit_text(
            "Введите наименование организации, в которую необходимо предоставить справку:"
        )
        await state.set_state(SalaryDoc.organization)
    await callback.answer()


@router.message(SalaryDoc.organization)
async def salary_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходима справка определенной формы – прикрепите файл (изображение, документ) или отправьте ссылку.\n"
        "Или нажмите 'Нет, не требуется'.",
        reply_markup=keyboard,
    )
    await state.set_state(SalaryDoc.form)


# ========== ОБРАБОТЧИКИ ДЛЯ PeriodDoc ==========


@router.message(PeriodDoc.purpose)
async def period_purpose(message: Message, state: FSMContext):
    purpose = message.text.strip()
    await state.update_data(purpose=purpose)
    await message.answer(
        "Введите наименование организации, в которую необходимо предоставить справку:"
    )
    await state.set_state(PeriodDoc.organization)


@router.message(PeriodDoc.organization)
async def period_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходима справка определенной формы – прикрепите файл или ссылку.",
        reply_markup=keyboard,
    )
    await state.set_state(PeriodDoc.form)


# ========== ОБРАБОТЧИКИ ДЛЯ CopyDoc ==========


@router.callback_query(CopyDoc.copy_type)
async def copy_type(callback: CallbackQuery, state: FSMContext):
    copy_type_ = "simple" if callback.data == "copy_simple" else "certified"
    await state.update_data(copy_type=copy_type_)
    await callback.message.edit_text(
        "Введите наименование организации, в которую необходимо предоставить копию:"
    )
    await state.set_state(CopyDoc.organization)
    await callback.answer()


@router.message(CopyDoc.organization)
async def copy_organization(message: Message, state: FSMContext, db: Database):
    org = message.text.strip()
    await state.update_data(organization=org)
    await finalize_request(message, state, db)


# ========== ОБРАБОТЧИКИ ДЛЯ VacationDoc ==========


@router.callback_query(VacationDoc.vacation_type)
async def vacation_type(callback: CallbackQuery, state: FSMContext):
    v_type = "regular" if callback.data == "vacation_regular" else "childcare"
    await state.update_data(vacation_type=v_type)
    await callback.message.edit_text(
        "Укажите, для чего нужна справка о периоде отпуска:"
    )
    await state.set_state(VacationDoc.purpose)
    await callback.answer()


@router.message(VacationDoc.purpose)
async def vacation_purpose(message: Message, state: FSMContext):
    purpose = message.text.strip()
    await state.update_data(purpose=purpose)
    await message.answer(
        "Введите наименование организации, в которую необходимо предоставить справку:"
    )
    await state.set_state(VacationDoc.organization)


@router.message(VacationDoc.organization)
async def vacation_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходима справка определенной формы – прикрепите файл или ссылку.",
        reply_markup=keyboard,
    )
    await state.set_state(VacationDoc.form)


# ========== ОБРАБОТЧИКИ ДЛЯ ChildDoc ==========


@router.message(ChildDoc.child_fullname)
async def child_fullname(message: Message, state: FSMContext):
    child_name = message.text.strip()
    await state.update_data(child_fullname=child_name)
    await message.answer("Введите дату рождения ребенка (например, 03.11.2020):")
    await state.set_state(ChildDoc.child_birth)


@router.message(ChildDoc.child_birth)
async def child_birth(message: Message, state: FSMContext):
    birth = message.text.strip()
    await state.update_data(child_birth=birth)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏕 Оздоровительный лагерь", callback_data="cert_camp"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏥 Санаторное лечение", callback_data="cert_sanatorium"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад в меню документов", callback_data="back_to_doc_menu"
                )
            ],
        ]
    )
    await message.answer("Выберите, какая справка нужна:", reply_markup=keyboard)
    await state.set_state(ChildDoc.certificate_type)


@router.callback_query(ChildDoc.certificate_type)
async def child_cert_type(callback: CallbackQuery, state: FSMContext):
    cert_type = "camp" if callback.data == "cert_camp" else "sanatorium"
    await state.update_data(certificate_type=cert_type)
    await callback.message.edit_text(
        "Введите наименование организации, в которую необходимо предоставить справку:"
    )
    await state.set_state(ChildDoc.organization)
    await callback.answer()


@router.message(ChildDoc.organization)
async def child_organization(message: Message, state: FSMContext, db: Database):
    org = message.text.strip()
    await state.update_data(organization=org)
    await finalize_request(message, state, db)


# ========== ОБРАБОТЧИКИ ДЛЯ ReferenceDoc ==========


@router.callback_query(ReferenceDoc.ref_type)
async def reference_type(callback: CallbackQuery, state: FSMContext):
    ref_type = "production" if callback.data == "ref_production" else "arbitrary"
    await state.update_data(ref_type=ref_type)
    await callback.message.edit_text(
        "Введите наименование организации, в которую необходимо предоставить характеристику:"
    )
    await state.set_state(ReferenceDoc.organization)
    await callback.answer()


@router.message(ReferenceDoc.organization)
async def reference_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходима характеристика определенной формы – прикрепите файл или ссылку.",
        reply_markup=keyboard,
    )
    await state.set_state(ReferenceDoc.form)


# ========== ОБРАБОТЧИКИ ДЛЯ PetitionDoc ==========


@router.message(PetitionDoc.petition_topic)
async def petition_topic(message: Message, state: FSMContext):
    topic = message.text.strip()
    await state.update_data(petition_topic=topic)
    await message.answer(
        "Укажите полное наименование организации, в которую необходимо предоставить ходатайство:"
    )
    await state.set_state(PetitionDoc.organization)


@router.message(PetitionDoc.organization)
async def petition_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходимо ходатайство определенной формы – прикрепите файл или ссылку.",
        reply_markup=keyboard,
    )
    await state.set_state(PetitionDoc.form)


# ========== ОБРАБОТЧИКИ ДЛЯ OtherDoc ==========


@router.message(OtherDoc.doc_name)
async def other_name(message: Message, state: FSMContext):
    doc_name = message.text.strip()
    await state.update_data(doc_name=doc_name)
    await message.answer(
        "Введите наименование организации, в которую необходимо предоставить документ:"
    )
    await state.set_state(OtherDoc.organization)


@router.message(OtherDoc.organization)
async def other_organization(message: Message, state: FSMContext):
    org = message.text.strip()
    await state.update_data(organization=org)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚫 Нет, не требуется", callback_data="attach_no"
                )
            ]
        ]
    )
    await message.answer(
        "Если необходим документ определенной формы – прикрепите файл или ссылку.",
        reply_markup=keyboard,
    )
    await state.set_state(OtherDoc.form)


# ========== ОБЩИЙ ОБРАБОТЧИК ДЛЯ ПРИКРЕПЛЕНИЯ ФОРМЫ ==========


@router.callback_query(F.data == "attach_no")
async def attach_no(callback: CallbackQuery, state: FSMContext, db: Database):
    await callback.message.edit_text("Форма не требуется. Заявка принята в обработку.")
    await finalize_request(callback.message, state, db)
    await callback.answer()


@router.message(F.document | F.photo | F.text)
async def attach_file(message: Message, state: FSMContext, db: Database):
    current_state = await state.get_state()
    logger.info(f"attach_file called with state: {current_state}")

    if not current_state:
        await message.answer(
            "Пожалуйста, начните с команды /start и выберите документ."
        )
        return

    if not current_state.endswith(":form"):
        await message.answer(
            "Сейчас не требуется прикреплять файл. Пожалуйста, следуйте инструкциям."
        )
        return

    try:
        attachment_data = {}

        if message.document:
            file = await message.bot.get_file(message.document.file_id)
            file_path = os.path.join(
                UPLOADS_DIR, f"doc_{message.from_user.id}_{message.document.file_name}"
            )
            await message.bot.download_file(file.file_path, file_path)
            attachment_data["file_path"] = file_path
            attachment_data["file_name"] = message.document.file_name
            attachment_data["type"] = "document"

        elif message.photo:
            photo = message.photo[-1]
            file = await message.bot.get_file(photo.file_id)
            file_path = os.path.join(
                UPLOADS_DIR, f"photo_{message.from_user.id}_{photo.file_unique_id}.jpg"
            )
            await message.bot.download_file(file.file_path, file_path)
            attachment_data["file_path"] = file_path
            attachment_data["file_name"] = f"photo_{photo.width}x{photo.height}.jpg"
            attachment_data["type"] = "photo"
        elif message.text:
            text = message.text.strip()
            if text.startswith(("http://", "https://", "t.me/", "www.")):
                attachment_data["file_path"] = text
                attachment_data["file_name"] = "link"
                attachment_data["type"] = "link"
            else:
                await message.answer(
                    "Пожалуйста, отправьте ссылку (начинающуюся с http://, https:// или t.me/) или файл."
                )
                return
        else:
            await message.answer(
                "Пожалуйста, прикрепите файл (изображение, документ) или ссылку."
            )
            return

        await state.update_data(
            file_path=attachment_data.get("file_path"),
            attachment_name=attachment_data.get("file_name"),
            attachment_type=attachment_data.get("type"),
        )
        await message.answer("✅ Файл получен. Заявка принята в обработку.")
        await finalize_request(message, state, db)
    except Exception as e:
        logger.error(f"Error in attach_file: {e}", exc_info=True)
        await message.answer(
            "❌ Произошла ошибка при обработке файла. Попробуйте позже."
        )


# ========== ФИНАЛИЗАЦИЯ И СОХРАНЕНИЕ В БД ==========


async def finalize_request(message: Message, state: FSMContext, db: Database):
    data = await state.get_data()
    user_id = message.from_user.id

    await db.save_document_request(
        user_id=user_id,
        doc_type=data.get("doc_type"),
        fullname=data.get("fullname"),
        phone=data.get("phone"),
        purpose=data.get("purpose"),
        period=data.get("period"),
        organization=data.get("organization"),
        file_path=data.get("file_path"),
        attachment_name=data.get("attachment_name"),
        attachment_type=data.get("attachment_type"),
        child_fullname=data.get("child_fullname"),
        child_birth=data.get("child_birth"),
        copy_type=data.get("copy_type"),
        vacation_type=data.get("vacation_type"),
        ref_type=data.get("ref_type"),
        petition_topic=data.get("petition_topic"),
        doc_name=data.get("doc_name"),
    )

    await message.answer(
        "✅ Запрашиваемый Вами документ будет готов в течение 3-х дней.\n"
        "О готовности документа Вам придет сообщение в Телеграм / сообщат по указанному телефону.\n\n"
        "Рады были помочь! Если возникнут дополнительные вопросы, мы всегда на связи!"
    )
    await state.clear()
