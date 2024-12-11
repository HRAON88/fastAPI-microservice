import base64
from pyrogram import Client


class TgClient:
    def __init__(self, client: Client):
        self.client = client

    async def parsing(self, limit: int, channel_ids: list[int]):
        data = {}
        for channel_id in channel_ids:
            async for message in self.client.get_chat_history(channel_id, limit):
                resp = await self.create_news_from_tg_message(message=message)
                if not resp:
                    continue
                text = resp["text"]
                if text in data:
                    data[text] = max(resp["photos"], data[text], key=len)
                else:
                    data[text] = resp["photos"]
        return {
            "count": len(data),
            "data": data,
        }

    async def create_news_from_tg_message(self, message):
        try:
            text = message.text or message.caption
            if not text:
                return None
            print("message with text:", text)
            if message.media_group_id:
                child_messages = await message.get_media_group()
            elif message.media:
                child_messages = [message]
            else:
                return
            print(f"message has {len(child_messages)} photos")
            photos = []
            for m in child_messages:
                media = await self.client.download_media(m.photo.file_id, in_memory=True)
                media.seek(0)
                photos.append(base64.b64encode(media.read()))
            return {
                "text": text,
                "photos": photos
            }
        except Exception as e:
            raise e
