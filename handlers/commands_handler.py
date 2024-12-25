from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions

from utils.chats_admins import AdminsManager
from lexicon.response_gens import you_have_to_answer, u_r_not_admin


commands_router = Router()


@commands_router.message(Command(commands='ban'))
async def ban_user(msg: Message, admins_manager: AdminsManager):
    if msg.from_user.id in admins_manager.chat_admins[msg.chat.id]:
        if msg.reply_to_message:
            await msg.bot.ban_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
            await msg.bot.delete_message(msg.chat.id, msg.message_id)
        else:
            await you_have_to_answer(msg)
    else:
        await u_r_not_admin(msg)


@commands_router.message(Command(commands='mute'))
async def mute_user(msg: Message, admins_manager: AdminsManager):
    if msg.from_user.id in admins_manager.chat_admins[msg.chat.id]:
        if msg.reply_to_message:
            # TODO добавить возможность задавать время мута
            await msg.bot.restrict_chat_member(msg.chat.id,
                                               msg.reply_to_message.from_user.id,
                                               ChatPermissions(can_send_messages = False),
                                               until_date = timedelta(minutes = 5))
            await msg.bot.delete_message(msg.chat.id, msg.message_id)
        else:
            await you_have_to_answer(msg)
    else:
        await u_r_not_admin(msg)


@commands_router.message(Command(commands='report'))
async def report_user(msg: Message, admins_manager: AdminsManager):
    if msg.reply_to_message:
        # TODO рассылкой уведомить админов о репорте
        print(msg.text)
        # await msg.bot.restrict_chat_member(msg.chat.id, msg.reply_to_message.from_user.id,
        #                                    ChatPermissions(can_send_messages=False), until_date=timedelta(minutes=5))
        # await msg.bot.delete_message(msg.chat.id, msg.message_id)
    else:
        await you_have_to_answer(msg)


# TODO написать старт для админов и юзверей
@commands_router.message(Command(commands='start'))
async def start_command(msg: Message, admins_manager: AdminsManager):
    pass
