import asyncio
import logging
import os
from aiogram import Bot
from aiogram.types import FSInputFile
from database.db import Database

logger = logging.getLogger(__name__)

# Словари для человекочитаемых названий
DOC_TYPE_NAMES = {
    "salary": "Справка о заработной плате",
    "period": "Справка о периоде работы",
    "copy": "Копия трудовой книжки",
    "vacation": "Справка об отпуске",
    "child": "Справка о необеспеченности ребенка путевкой",
    "reference": "Характеристика",
    "petition": "Ходатайство",
    "other": "Другой документ"
}

PURPOSE_NAMES = {
    "house": "🏠 Кредит на жильё",
    "car": "🚗 Кредит на машину",
    "improve": "🏡 Улучшение жилищных условий",
    "tax": "📄 Налоговая",
    "consumer": "🛒 Потребительский кредит",
    "installment": "📦 Рассрочка на товары",
    "other": "✏️ Другое"
}

PERIOD_NAMES = {
    "3": "3 месяца",
    "6": "6 месяцев",
    "12": "12 месяцев"
}

COPY_TYPE_NAMES = {
    "simple": "📄 Ксерокопия",
    "certified": "📜 Заверенная подписью и печатью"
}

VACATION_TYPE_NAMES = {
    "regular": "🏖 Трудовой или социальный отпуск",
    "childcare": "👶 Отпуск по уходу за ребенком"
}

REF_TYPE_NAMES = {
    "production": "🏭 Производственная характеристика",
    "arbitrary": "📄 В произвольной форме"
}

CERTIFICATE_TYPE_NAMES = {
    "camp": "🏕 В оздоровительный лагерь",
    "sanatorium": "🏥 Для санаторного лечения"
}

async def monitor_new_requests(bot: Bot, db: Database, chat_id: str, interval: int = 10):
    if not chat_id:
        logger.warning("NOTIFICATION_CHAT_ID не задан, уведомления отключены")
        return

    logger.info(f"Мониторинг новых заявок запущен, интервал {interval} сек, чат {chat_id}")

    while True:
        try:
            last_id = await db.get_last_processed_notification_id()
            new_requests = await db.get_new_document_requests(last_id)

            if new_requests:
                logger.info(f"Найдено {len(new_requests)} новых заявок")
                for req in new_requests:
                    try:
                        await send_notification(bot, chat_id, req)
                    except Exception as e:
                        logger.error(f"Ошибка при отправке уведомления для заявки #{req['id']}: {e}", exc_info=True)
                    finally:
                        await db.update_last_processed_notification_id(req['id'])
            else:
                logger.debug("Новых заявок нет")

        except Exception as e:
            logger.error(f"Критическая ошибка в мониторинге: {e}", exc_info=True)

        await asyncio.sleep(interval)

async def send_notification(bot: Bot, chat_id: str, request: dict):
    """Отправляет уведомление: сначала текст, затем медиа (если есть локальный файл или ссылка)."""
    doc_name = DOC_TYPE_NAMES.get(request.get('doc_type'), request.get('doc_type'))

    lines = []
    lines.append("🆕 НОВАЯ ЗАЯВКА НА ДОКУМЕНТ")
    lines.append("")
    lines.append(f"Тип: {doc_name}")
    lines.append(f"От: {request.get('fullname')} (ID: {request.get('user_id')})")
    lines.append(f"Организация: {request.get('organization', 'не указана')}")

    if request.get('purpose'):
        purpose_code = request['purpose']
        purpose_text = PURPOSE_NAMES.get(purpose_code, purpose_code)
        lines.append(f"Цель: {purpose_text}")

    if request.get('period'):
        period_code = request['period']
        if period_code == "other":
            lines.append("Период: иной (указан при оформлении)")
        else:
            period_text = PERIOD_NAMES.get(period_code, f"{period_code} месяцев")
            lines.append(f"Период: {period_text}")

    if request.get('child_fullname'):
        child_line = f"Ребёнок: {request['child_fullname']}"
        if request.get('child_birth'):
            child_line += f" ({request['child_birth']})"
        lines.append(child_line)

    if request.get('copy_type'):
        copy_text = COPY_TYPE_NAMES.get(request['copy_type'], request['copy_type'])
        lines.append(f"Тип копии: {copy_text}")

    if request.get('vacation_type'):
        vac_text = VACATION_TYPE_NAMES.get(request['vacation_type'], request['vacation_type'])
        lines.append(f"Тип отпуска: {vac_text}")

    if request.get('ref_type'):
        ref_text = REF_TYPE_NAMES.get(request['ref_type'], request['ref_type'])
        lines.append(f"Тип характеристики: {ref_text}")

    if request.get('certificate_type'):
        cert_text = CERTIFICATE_TYPE_NAMES.get(request['certificate_type'], request['certificate_type'])
        lines.append(f"Тип справки: {cert_text}")

    if request.get('petition_topic'):
        lines.append(f"Тема ходатайства: {request['petition_topic']}")

    if request.get('doc_name'):
        lines.append(f"Документ: {request['doc_name']}")

    text = "\n".join(lines)

    # Отправляем текст
    await bot.send_message(chat_id, text)

    # Обрабатываем вложение
    attachment_type = request.get('attachment_type')
    attachment_path = request.get('file_path')  # теперь это путь к файлу или ссылка
    attachment_name = request.get('attachment_name', 'файл')

    if not attachment_path:
        return

    try:
        if attachment_type == 'photo':
            if os.path.exists(attachment_path):
                await bot.send_photo(chat_id, photo=FSInputFile(attachment_path))
                logger.info(f"Фото отправлено из файла {attachment_path}")
            else:
                await bot.send_message(chat_id, f"⚠️ Файл фото не найден на сервере: {attachment_path}")
        elif attachment_type == 'document':
            if os.path.exists(attachment_path):
                await bot.send_document(chat_id, document=FSInputFile(attachment_path))
                logger.info(f"Документ отправлен из файла {attachment_path}")
            else:
                await bot.send_message(chat_id, f"⚠️ Файл документа не найден на сервере: {attachment_path}")
        elif attachment_type == 'link':
            await bot.send_message(chat_id, f"🔗 Ссылка: {attachment_path}")
        else:
            # Неизвестный тип – просто выводим путь
            await bot.send_message(chat_id, f"📎 Прикреплён файл: {attachment_name} (путь: {attachment_path})")
    except Exception as e:
        logger.error(f"Ошибка отправки медиа: {e}")
        await bot.send_message(chat_id, f"⚠️ Ошибка при отправке вложения. Путь: {attachment_path}")