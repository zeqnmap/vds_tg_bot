from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.inline import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: CallbackQuery):
    """Возврат в главное меню"""
    text = "👋 **Главное меню**\n\nВыберите действие:"
    await callback.message.edit_text(
        text, reply_markup=get_main_menu_keyboard(), parse_mode="Markdown"
    )
    await callback.answer()
