import asyncio
from aiogram.types import Message

from lexicon.response_text import you_have_to_answer_txt, u_r_not_admin_txt


async def you_have_to_answer(msg: Message):
    await msg.bot.delete_message(msg.chat.id, msg.message_id)
    response = await msg.answer(you_have_to_answer_txt)
    await asyncio.sleep(4)
    await msg.bot.delete_message(msg.chat.id, response.message_id)


async def u_r_not_admin(msg: Message):
    await msg.bot.delete_message(msg.chat.id, msg.message_id)
    response = await msg.answer(f"{u_r_not_admin_txt}{msg.from_user.username}")
    await asyncio.sleep(3)
    await msg.bot.delete_message(msg.chat.id, response.message_id)
