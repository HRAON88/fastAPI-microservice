import os

from pyrogram import Client

from app.services.telegram import TgClient


async def get_telegram() -> TgClient:
    session = Client("my_account", workdir=os.getcwd())
    await session.start()
    yield TgClient(session)
    await session.stop()
