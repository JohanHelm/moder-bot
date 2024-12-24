import asyncio
from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from utils.chats_admins import AdminsManager

commands_router = Router()

@commands_router.message(Command(commands='ban'))
async def ban_user(msg: Message, admins_manager: AdminsManager):
    if msg.from_user.id in admins_manager.chat_admins[msg.chat.id]:
        if msg.reply_to_message:
            await msg.bot.ban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
            await msg.bot.delete_message(msg.chat.id, msg.message_id)
        else:
            response = await msg.answer("оставьте ссылку на сообщения пользователя")
            await asyncio.sleep(3)
            await msg.bot.delete_message(msg.chat.id, response.message_id)
    else:
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
        response = await msg.answer(f"Вы не являетесь администратором данного сообщества @{msg.from_user.username}")
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, response.message_id)


@commands_router.message(Command(commands='mute'))
async def mute_user(msg: Message, admins_manager: AdminsManager):
    if msg.from_user.id in admins_manager.chat_admins[msg.chat.id]:
        if msg.reply_to_message:
            await msg.bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, ChatPermissions(can_send_messages = False), until_date = timedelta(minutes = 5))
            await msg.bot.delete_message(msg.chat.id, msg.message_id)
        else:
            response = await msg.answer("оставьте ссылку на сообщения пользователя")
            await asyncio.sleep(3)
            await msg.bot.delete_message(msg.chat.id, response.message_id)
    else:
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
        response = await msg.answer(f"Вы не являетесь администратором данного сообщества @{msg.from_user.username}")
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, response.message_id)


@commands_router.message(Command(commands='report'))
async def report_user(msg: Message, admins_manager: AdminsManager):
    pass


@commands_router.message(Command(commands='start'))
async def ban_user(msg: Message, admins_manager: AdminsManager):
    pass
