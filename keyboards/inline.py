from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню с 5 inline-кнопками (2-2-1)"""
    builder = InlineKeyboardBuilder()
    builder.button(text="👷 Социализация", callback_data="social")
    builder.button(text="️📚 Обучение", callback_data="study")
    builder.button(text="🚎 Транспорт", callback_data="transport")
    builder.button(text="❓ Частые вопросы", callback_data="usual_q")
    builder.button(text="⁉️ Особые вопросы", callback_data="unusual_q")
    builder.button(text="📄 Документы", callback_data="doc_menu")
    builder.adjust(2, 2, 1)
    return builder.as_markup()


# ==================== SOCIAL ====================


def get_social_submenu_keyboard() -> InlineKeyboardMarkup:
    """Подменю для раздела Социализация"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🏥 ЗДРАВПУНКТ", callback_data="social_about")
    builder.button(text="🙏 УСЛУГИ", callback_data="social_contacts")
    builder.button(text="🌳 ЭКОЛОГИЯ", callback_data="social_esg")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2, 1)
    return builder.as_markup()


# ==================== STUDY ====================


def get_study_submenu_keyboard() -> InlineKeyboardMarkup:
    """Подменю для раздела Обучение"""
    builder = InlineKeyboardBuilder()
    builder.button(text="💻 ПЛАТФОРМА", callback_data="platform")
    builder.button(text="⛪️ ЦЕРКОВЬ", callback_data="church")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2, 1)
    return builder.as_markup()


# ==================== TRANSPORT ====================


def get_transport_submenu_keyboard() -> InlineKeyboardMarkup:
    """Подменю для раздела Транспорт"""
    builder = InlineKeyboardBuilder()
    builder.button(text="📅 РАСПИСАНИЕ", callback_data="schedule")
    builder.button(text="🚗 ПАРКОВКА", callback_data="parking")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2, 1)
    return builder.as_markup()


# ==================== USUAL ====================


def get_usual_submenu_keyboard() -> InlineKeyboardMarkup:
    """Подменю для раздела Обычных вопросов"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🪥 ГИГИЕНА", callback_data="hygiene")
    builder.button(text="🍽️ ПИТАНИЕ", callback_data="canteen")
    builder.button(text="💸 ЗП", callback_data="salary")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2, 1)
    return builder.as_markup()


# ==================== DOCS ====================

def get_doc_menu_keyboard() -> InlineKeyboardMarkup:
    """Меню выбора документа (8 пунктов)"""
    builder = InlineKeyboardBuilder()
    builder.button(text="1️⃣", callback_data="doc_salary")
    builder.button(text="2️⃣", callback_data="doc_period")
    builder.button(text="3️⃣", callback_data="doc_copy")
    builder.button(text="4️⃣", callback_data="doc_vacation")
    builder.button(text="5️⃣", callback_data="doc_child")
    builder.button(text="6️⃣", callback_data="doc_reference")
    builder.button(text="7️⃣", callback_data="doc_petition")
    builder.button(text="8️⃣", callback_data="doc_other")
    builder.button(text="🔙 Назад", callback_data="back_to_main")
    builder.adjust(2, 2, 2, 2, 1)
    return builder.as_markup()