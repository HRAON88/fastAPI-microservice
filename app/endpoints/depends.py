import os
from dotenv import load_dotenv
from pyrogram import Client
from app.services.telegram import TgClient
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
SESSION_STRING = os.getenv('SESSION_STRING')
# Глобальная переменная для хранения клиента
_telegram_client: Optional[TgClient] = None


async def get_telegram():
    """
    Возвращает существующий клиент или создает новый, если клиент не существует
    """
    global _telegram_client

    if _telegram_client is not None and _telegram_client.client.is_connected:
        return _telegram_client

    try:
        session = Client(
            "my_session_for_parser",
            session_string=SESSION_STRING,
        )

        await session.start()
        _telegram_client = TgClient(session)
        logger.info("Created new Telegram client session")
        return _telegram_client

    except Exception as e:
        logger.error(f"Error during session initialization: {str(e)}")
        if session and session.is_connected:
            await session.stop()
        raise