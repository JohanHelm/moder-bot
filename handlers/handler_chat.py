import asyncio
import re
from datetime import timedelta

import aiogram.exceptions
from aiogram import F, Router, enums
from aiogram.filters import Command, StateFilter, ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN, ADMINISTRATOR, CREATOR
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, URLInputFile, ChatPermissions, ChatMemberUpdated, MessageReactionUpdated


from handlers.utils.Utility import Censorship

router_channel = Router()

# @router_channel.message(IS_ADMIN)
# async def send_echo(message: Message):
#     await message.reply(text=message.text)

@router_channel.message(lambda message: message.chat.type in (enums.chat_type.ChatType.GROUP, enums.chat_type.ChatType.SUPERGROUP) and message.content_type == "text")
async def handle_channel_post(msg: Message):
    flag = await Censorship.main_filter(msg.text)

    if flag >= float(0.34):
        await msg.answer(f'Вы написали нецензурное слово')
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
    print(*msg.chat, sep='\n')

    # print(*msg.from_user, sep='\n')
    # print(type(ChatMemberUpdatedFilter(IS_MEMBER).member_status_changed))
    # print(ChatMemberUpdatedFilter(IS_MEMBER).member_status_changed)
    # print(await msg.bot.get_chat_administrators(msg.chat.id))
    if ChatMemberUpdatedFilter(IS_ADMIN).member_status_changed == ADMINISTRATOR or CREATOR:
        if msg.text.startswith("/ban"):
            if msg.reply_to_message:
                await msg.bot.ban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
                await msg.bot.delete_message(msg.chat.id, msg.message_id)
            else:
                await msg.answer("оставьте ссылку на сообщения пользователя")
        elif msg.text.startswith("/mute"):
            if msg.reply_to_message:
                await msg.bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id, ChatPermissions(can_send_messages = False), until_date = timedelta(minutes = 5))
                await msg.bot.delete_message(msg.chat.id, msg.message_id)
            else:
                await msg.answer("оставьте ссылку на сообщения пользователя")
#



#функция приветствия
@router_channel.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):

    msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.first_name} {event.from_user.last_name}") #, reply_to_message_id = "172" )
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