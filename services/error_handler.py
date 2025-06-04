import logging
import httpx
import os

# Конфигурация Telegram бота (лучше вынести в переменные окружения)

TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']


async def send_telegram_notification(error_details: str):
    """
    Отправляет уведомление об ошибке в Telegram чат
    :param error_details: Текст сообщения об ошибке
    """
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                telegram_url,
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": f"🚨 FastAPI Error Alert\n\n{error_details}",
                    "parse_mode": "Markdown"
                },
                timeout=10.0
            )
            response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to send Telegram notification: {str(e)}")
