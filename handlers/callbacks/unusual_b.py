from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline import (
get_social_submenu_keyboard
)
from utils.logger_conf import setup_logger

logger = setup_logger(__name__)

router = Router()