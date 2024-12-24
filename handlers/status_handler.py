import asyncio

from aiogram import F, Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN, ADMINISTRATOR, CREATOR
from aiogram.types import Message, ChatMemberUpdated, MessageReactionUpdated


status_router = Router()


#функция приветствия
@status_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):

    msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.username} {event.from_user.last_name}")
    await asyncio.sleep(3)
    await msg.bot.delete_message(msg.chat.id, msg.message_id)


#тригер для пользователей переведённых в админы
@status_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated):

    msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.first_name} {event.from_user.last_name}") #, reply_to_message_id = "172" )
    await asyncio.sleep(3)
    await msg.bot.delete_message(msg.chat.id, msg.message_id)

# тригер для ушедших пользователей
@status_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER << IS_MEMBER))
async def new_member(event: ChatMemberUpdated):


    pass
# тригер для реакций
@status_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated):

    pass

#тригер для ответов
@status_router.message(F.reply_to_message)
async def reply(msg: Message):

    pass