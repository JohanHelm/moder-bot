# -*- coding: utf-8 -*-
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from handlers.handler_chat import router_channel



async def start_bot():
    bot = Bot(token="7760139416:AAFMz8W5boLSg_lb-jHHWfBwq8BTUZVk6RA", default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware()
    dp.include_router(router_channel)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Запускаем бота
    asyncio.run(start_bot())


# хрен,