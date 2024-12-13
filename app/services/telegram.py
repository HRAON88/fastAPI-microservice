import base64
import logging
from typing import Dict, Any, List, Optional
from pyrogram import Client
from pyrogram.types import Message

logger = logging.getLogger(__name__)


class TgClient:
    def __init__(self, client: Client):
        self.client = client

    async def parsing(self, limit: int, channel_ids: List[int]) -> Dict[str, Any]:
        """
        Парсит сообщения из указанных каналов
        """
        try:
            data = {}
            total_processed = 0

            for channel_id in channel_ids:
                try:
                    logger.info(f"Начало парсинга канала {channel_id}")

                    # Проверяем доступ к каналу
                    try:
                        await self.client.get_chat(channel_id)
                    except Exception as e:
                        logger.error(f"Не удалось получить доступ к каналу {channel_id}: {str(e)}")
                        continue

                    async for message in self.client.get_chat_history(channel_id, limit=limit):
                        try:
                            resp = await self.create_news_from_tg_message(message)
                            if not resp:
                                continue

                            text = resp["text"]
                            if text in data:
                                # Если текст уже существует, выбираем набор фото с большим количеством
                                data[text] = max(resp["photos"], data[text], key=len)
                            else:
                                data[text] = resp["photos"]

                            total_processed += 1

                        except Exception as msg_error:
                            logger.error(f"Ошибка при обработке сообщения: {str(msg_error)}")
                            continue

                except Exception as channel_error:
                    logger.error(f"Ошибка при парсинге канала {channel_id}: {str(channel_error)}")
                    continue

            logger.info(f"Парсинг завершен. Обработано сообщений: {total_processed}, уникальных записей: {len(data)}")

            return {
                "count": len(data),
                "data": data,
            }

        except Exception as e:
            logger.error(f"Критическая ошибка при парсинге: {str(e)}", exc_info=True)
            raise

    async def create_news_from_tg_message(self, message: Message) -> Optional[Dict[str, Any]]:
        """
        Создает новость из сообщения Telegram
        """
        try:
            # Получаем текст сообщения
            text = message.text or message.caption
            if not text:
                return None

            logger.debug(f"Обработка сообщения: {text[:100]}...")

            # Получаем медиафайлы
            try:
                if message.media_group_id:
                    child_messages = await message.get_media_group()
                elif message.media:
                    child_messages = [message]
                else:
                    return None

                logger.debug(f"Найдено {len(child_messages)} медиафайлов")

            except Exception as media_error:
                logger.error(f"Ошибка при получении медиафайлов: {str(media_error)}")
                return None

            # Обрабатываем фотографии
            photos = []
            for m in child_messages:
                try:
                    if not m.photo:
                        continue

                    media = await self.client.download_media(m.photo.file_id, in_memory=True)
                    if not media:
                        continue

                    media.seek(0)
                    photo_data = base64.b64encode(media.read()).decode('utf-8')
                    photos.append(photo_data)

                except Exception as photo_error:
                    logger.error(f"Ошибка при обработке фото: {str(photo_error)}")
                    continue

            if not photos:
                return None

            return {
                "text": text,
                "photos": photos
            }

        except Exception as e:
            logger.error(f"Ошибка в create_news_from_tg_message: {str(e)}", exc_info=True)
            return None