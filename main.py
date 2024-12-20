# -*- coding: utf-8 -*-
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

from database import db
from handlers.handler_chat import router_channel
import nltk
nltk.download('punkt_tab')


async def get_my_id(bot: Bot) -> int:
    my_user_data = await bot.get_me()
    return my_user_data.id


async def refresh_chats_admins(bot: Bot):
    await db.connect()
    chats =


async def get_chats_from_db()


async def start_bot():
    bot = Bot(token="5417896659:AAGgDrekLFFyDX6iylJHGQwHProR-itsabA", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # print(*await bot.get_chat_administrators('-1002400455551'), sep='\n')
    my_id = await get_my_id(bot)
    print(my_id)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware()
    dp.include_router(router_channel)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Запускаем бота
    asyncio.run(start_bot())


