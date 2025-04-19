import base64
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from pyrogram import Client
from pyrogram.types import Message, InputMediaDocument

DEFAULT_CHAT_ID = 5019406849

logger = logging.getLogger(__name__)

BACKUP_DIR_ENV = os.getenv("BACKUP_DIR", "")
if BACKUP_DIR_ENV:
    BACKUP_DIR = Path(BACKUP_DIR_ENV)
elif os.path.exists("./backups"):
    BACKUP_DIR = Path("./backups")
elif os.path.exists("./app/backups"):
    BACKUP_DIR = Path("./app/backups")
else:
    BACKUP_DIR = Path("/app/app/backups")

class TgClient:
    def __init__(self, client: Client):
        self.client = client

    async def parsing(self, limit: int, channel_ids: List[int]) -> Dict[str, Any]:
        try:
            data = {}
            total_processed = 0
            posts_processed = 0

            for channel_id in channel_ids:
                try:
                    logger.info(f"Начало парсинга канала {channel_id}")

                    try:
                        await self.client.get_chat(channel_id)
                    except Exception as e:
                        logger.error(f"Не удалось получить доступ к каналу {channel_id}: {str(e)}")
                        continue

                    async for message in self.client.get_chat_history(channel_id):
                        if posts_processed >= limit:
                            break

                        try:
                            resp = await self.create_news_from_tg_message(message)
                            if not resp:
                                continue

                            text = resp["text"]
                            created_at = resp["created_at"]

                            if text in data:
                                if len(resp["photos"]) > len(data[text]["photos"]):
                                    data[text] = {
                                        "photos": resp["photos"],
                                        "created_at": created_at
                                    }
                            else:
                                data[text] = {
                                    "photos": resp["photos"],
                                    "created_at": created_at
                                }

                            total_processed += 1
                            posts_processed += 1

                        except Exception as msg_error:
                            logger.error(f"Ошибка при обработке сообщения: {str(msg_error)}")
                            continue

                except Exception as channel_error:
                    logger.error(f"Ошибка при парсинге канала {channel_id}: {str(channel_error)}")
                    continue

            logger.info(f"Парсинг завершен. Обработано сообщений: {total_processed}, уникальных записей: {len(data)}")

            return {
                "count": len(data),
                "data": {
                    text: {
                        "photos": item["photos"],
                        "created_at": item["created_at"]
                    } for text, item in data.items()
                }
            }

        except Exception as e:
            logger.error(f"Ошибка парсинга: {str(e)}")
            raise

    async def create_news_from_tg_message(self, message: Message) -> Optional[Dict[str, Any]]:
        try:
            text = message.text or message.caption
            if not text:
                return None

            try:
                if message.media_group_id:
                    child_messages = await message.get_media_group()
                elif message.media:
                    child_messages = [message]
                else:
                    return None

            except Exception as media_error:
                logger.error(f"Ошибка получения медиа: {str(media_error)}")
                return None

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

                except Exception:
                    continue

            if not photos:
                return None

            return {
                "text": text,
                "photos": photos,
                "created_at": message.date.timestamp()
            }

        except Exception as e:
            logger.error(f"Ошибка создания новости: {str(e)}")
            return None

    async def send_backup(self, backup: str, custom_chat_id: Union[int, str]):
        daily_dir = BACKUP_DIR / "daily"
        backup_path = daily_dir / backup
        
        if not backup_path.exists():
            backup_path = BACKUP_DIR / backup
            
        if backup_path.exists():
            try:
                target_chat_id = custom_chat_id
                if target_chat_id.startswith('-'):
                    target_chat_id = int(target_chat_id)

                else:
                    if isinstance(target_chat_id, str) and not target_chat_id.startswith('@'):
                        target_chat_id = f"@{target_chat_id}"

                print(target_chat_id)
                await self.client.send_document(
                    chat_id=target_chat_id,
                    document=str(backup_path),
                    caption=f"Backup file: {backup}"
                )
                return True
                    
            except Exception as e:
                logger.error(f"Ошибка отправки бекапа: {str(e)}")
                return False
        else:
            logger.warning(f"Файл не найден: {backup}")
            return False
            
    async def list_backups(self):
        backups = []
        
        daily_dir = BACKUP_DIR / "daily"
        if daily_dir.exists():
            files = list(daily_dir.glob("*.sql.gz"))
            backups.extend([f.name for f in files])
            
        if BACKUP_DIR.exists():
            files = list(BACKUP_DIR.glob("*.sql.gz"))
            backups.extend([f.name for f in files 
                           if f.name not in backups])
            
        return backups
