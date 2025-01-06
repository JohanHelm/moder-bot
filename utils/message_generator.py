import asyncio

from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from utils.chats_admins import AdminsManager
from lexicon.response_text import you_have_to_answer_txt, u_r_not_admin_txt, curse_moder_txt, report_from_user_txt

async def notify_chat_admins_on_report(admins_manager: AdminsManager, msg: Message):
    admins_chat_id = admins_manager.chats_for_chat_admins[msg.chat.id]
    await msg.bot.send_message(admins_chat_id, f"{report_from_user_txt}{msg.from_user.username}")
    await msg.bot.forward_message(admins_chat_id, msg.chat.id, msg.reply_to_message.message_id)
    # for admin_id in admins_manager.chat_admins[msg.chat.id]:
    #     try:
    #         await msg.bot.send_message(admin_id, f"{report_from_user_txt}{msg.from_user.username}")
    #         await msg.bot.forward_message(admin_id, msg.chat.id, msg.reply_to_message.message_id)
    #     except TelegramForbiddenError:
    #         print(f"bot was blocked by the admin with id {admin_id}")


async def notify_chat_admins_on_curse(admins_manager: AdminsManager, msg: Message):
    admins_chat_id = admins_manager.chats_for_chat_admins[msg.chat.id]
    await msg.bot.send_message(admins_chat_id, f"@{msg.from_user.username} {curse_moder_txt}")
    await msg.bot.forward_message(admins_chat_id, msg.chat.id, msg.message_id)

    # for admin_id in admins_manager.chat_admins[msg.chat.id]:
    #     try:
    #         await msg.bot.send_message(admin_id, f"@{msg.from_user.username} {curse_moder_txt}")
    #         await msg.bot.forward_message(admin_id, msg.chat.id, msg.message_id)
    #     except TelegramForbiddenError:
    #         print(f"bot was blocked by the admin with id {admin_id}")


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
