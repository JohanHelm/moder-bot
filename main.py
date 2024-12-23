import asyncio
import logging
import nltk
import dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from handlers.handler_chat import router_channel
from database.chats_admins import AdminsUpdater

nltk.download('punkt_tab')


async def start_bot():
    dotenv.load_dotenv("secrets/.env")
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    au = AdminsUpdater("moder_bot.db", bot)
    await au.update_admins()
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware()
    dp.include_router(router_channel)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())


