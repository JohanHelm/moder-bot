import asyncio
import logging


import nltk

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from config_data.config import load_config
from handlers.moder_handler import moder_router
from handlers.commands_handler import commands_router
from handlers.status_handler import status_router
from utils.chats_admins import AdminsManager


nltk.download("punkt_tab")


async def start_bot():
    config = load_config("confidential/.env")
    # config = load_config()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    admins_manager = AdminsManager("moder_bot.db", bot)
    await admins_manager.update_admins()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(commands_router)
    dp.include_router(moder_router)
    dp.include_router(status_router)
    dp.workflow_data.update({"admins_manager": admins_manager})
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_bot())


