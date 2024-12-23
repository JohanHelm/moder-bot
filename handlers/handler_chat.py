import asyncio
import re
from datetime import timedelta
import os

import aiogram.exceptions
from aiogram import F, Router, enums
from aiogram.filters import Command, StateFilter, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN, ADMINISTRATOR, CREATOR
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, URLInputFile, ChatPermissions, ChatMemberUpdated, MessageReactionUpdated

from handlers.utils.Utility import Censorship
from database.chats_admins import AdminsManager


router_channel = Router()

# TODO remove this hardcode
chats_me_admin = [-1002400455551]
chat_admins = {-1002400455551: [5417896659, 1608080468]}

@router_channel.message(lambda message: message.chat.id in chats_me_admin and message.content_type == "text")
async def handle_channel_post(msg: Message):
    flag = await Censorship.main_filter(msg.text)

    if flag >= float(0.34):
        response = await msg.answer(f'Вы написали нецензурное слово @{msg.from_user.username}')
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, response.message_id)
    # print(*msg.chat, sep='\n')

    if msg.text.startswith("/ban"):
        if msg.from_user.id in chat_admins[msg.chat.id]:
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

    if msg.text.startswith("/mute"):
        if msg.from_user.id in chat_admins[msg.chat.id]:
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





#функция приветствия
@router_channel.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):

    msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.username} {event.from_user.last_name}")
    await asyncio.sleep(3)
    await msg.bot.delete_message(msg.chat.id, msg.message_id)


#тригер для пользователей переведённых в админы
@router_channel.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):

    msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.first_name} {event.from_user.last_name}") #, reply_to_message_id = "172" )
    await asyncio.sleep(3)
    await msg.bot.delete_message(msg.chat.id, msg.message_id)

# тригер для ушедших пользователей
@router_channel.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER << IS_MEMBER))
async def new_member(event: ChatMemberUpdated):


    pass
# тригер для реакций
@router_channel.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated):

    pass

#тригер для ответов
@router_channel.message(F.reply_to_message)
async def reply(msg: Message):

    pass