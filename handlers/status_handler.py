import asyncio

from aiogram import F, Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER, IS_ADMIN, ADMINISTRATOR, CREATOR
from aiogram.types import Message, ChatMemberUpdated, MessageReactionUpdated, ChatPermissions

from utils.chats_admins import AdminsManager
from lexicon.response_text import wellcome

status_router = Router()


#функция приветствия
@status_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated, admins_manager: AdminsManager):
    msg = await event.answer(text=wellcome)
    await msg.bot.restrict_chat_member(event.chat.id, event.new_chat_member.user.id,
                                       ChatPermissions(can_send_messages=False))
    await admins_manager.add_new_user(event.from_user.id, event.from_user.is_bot, event.from_user.first_name, event.from_user.last_name, event.from_user.username)
    await asyncio.sleep(10)
    await msg.bot.restrict_chat_member(event.chat.id, event.new_chat_member.user.id,
                                       ChatPermissions(can_send_messages=True))
    # await msg.bot.ban_chat_member(event.chat.id, event.new_chat_member.user.id, revoke_messages=True)
    await msg.bot.delete_message(msg.chat.id, msg.message_id)

    # # TODO направлять нового пользователя на сообщение с правилами и дальше в бота в ФСМ с анкетой
    # # TODO до одобрения админами не давать доступ к чату(читать, писать, видеть юзверей)
    # msg = await event.answer(text = f"Здравствуй как у тебя {event.from_user.username} {event.from_user.last_name}")
    # await asyncio.sleep(3)
    # await msg.bot.delete_message(msg.chat.id, msg.message_id)
    # # TODO Если админы не одобрили пользователя кикнуть его, закинуть его в бд с отметкой о кике
    # # TODO После одобрения админами дать доступ юзверю к чату, закинуть его в бд


# TODO Отметить в бд ушедшего юзверя
# TODO Отметить в БД сам ушол или забанили
# тригер для ушедших пользователей
@status_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER << IS_MEMBER))
async def new_member(event: ChatMemberUpdated):
    pass


#тригер для пользователей переведённых в админы
@status_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_ADMIN))
async def promote_to_admin(event: ChatMemberUpdated, admins_manager: AdminsManager):
    await admins_manager.add_new_admin(event.chat.id, event.new_chat_member.user.id)


#тригер для пользователей переведённых из админа в обычного пользователя
@status_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER << IS_ADMIN))
async def demote_to_user(event: ChatMemberUpdated, admins_manager: AdminsManager):
    await admins_manager.from_admin_to_user(event.chat.id, event.new_chat_member.user.id)




# тригер для реакций
@status_router.message_reaction()
async def message_reaction_handler(message_reaction: MessageReactionUpdated):

    pass

#тригер для ответов
@status_router.message(F.reply_to_message)
async def reply(msg: Message):

    pass