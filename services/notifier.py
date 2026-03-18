import asyncio
import logging
from aiogram import Bot
from database.db import Database

logger = logging.getLogger(__name__)

async def monitor_new_requests(bot: Bot, db: Database, chat_id: str, interval: int = 10):
    """
    Фоновая задача: каждые interval секунд проверяет новые заявки в БД
    и отправляет уведомление в указанный чат.
    """
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
                    await send_notification(bot, chat_id, req)
                    # Обновляем last_id после каждой успешной отправки
                    await db.update_last_processed_notification_id(req['id'])
            else:
                logger.debug("Новых заявок нет")

        except Exception as e:
            logger.error(f"Ошибка в мониторинге заявок: {e}", exc_info=True)

        await asyncio.sleep(interval)


async def send_notification(bot: Bot, chat_id: str, request: dict):
    """Формирует и отправляет сообщение о новой заявке"""
    doc_type_names = {
        "salary": "Справка о заработной плате",
        "period": "Справка о периоде работы",
        "copy": "Копия трудовой книжки",
        "vacation": "Справка об отпуске",
        "child": "Справка о необеспеченности ребенка путевкой",
        "reference": "Характеристика",
        "petition": "Ходатайство",
        "other": "Другой документ"
    }

    doc_name = doc_type_names.get(request.get('doc_type'), request.get('doc_type'))

    text = f"🆕 **Новая заявка на документ**\n\n"
    text += f"**Тип:** {doc_name}\n"
    text += f"**От:** {request.get('fullname')} (ID: {request.get('user_id')})\n"
    text += f"**Организация:** {request.get('organization', 'не указана')}\n"

    if request.get('purpose'):
        text += f"**Цель:** {request['purpose']}\n"
    if request.get('period'):
        text += f"**Период:** {request['period']}\n"
    if request.get('child_fullname'):
        text += f"**Ребёнок:** {request['child_fullname']} ({request.get('child_birth', '')})\n"
    if request.get('copy_type'):
        text += f"**Тип копии:** {'заверенная' if request['copy_type']=='certified' else 'ксерокопия'}\n"
    if request.get('vacation_type'):
        text += f"**Тип отпуска:** {'по уходу за ребёнком' if request['vacation_type']=='childcare' else 'обычный'}\n"
    if request.get('ref_type'):
        text += f"**Тип характеристики:** {'производственная' if request['ref_type']=='production' else 'произвольная'}\n"
    if request.get('petition_topic'):
        text += f"**Тема ходатайства:** {request['petition_topic']}\n"
    if request.get('doc_name'):
        text += f"**Документ:** {request['doc_name']}\n"

    if request.get('attachment'):
        attach_type = request.get('attachment_type', 'file')
        if attach_type == 'photo':
            text += f"\n📷 **Прикреплено фото**"
        elif attach_type == 'document':
            text += f"\n📎 **Прикреплён документ:** {request['attachment_name']}"
        elif attach_type == 'link':
            text += f"\n🔗 **Ссылка:** {request['attachment']}"
        else:
            text += f"\n📎 **Прикреплён файл:** {request['attachment_name']}"

    try:
        await bot.send_message(chat_id, text, parse_mode="Markdown")
        logger.info(f"Уведомление о заявке #{request['id']} отправлено")
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление в чат {chat_id}: {e}")