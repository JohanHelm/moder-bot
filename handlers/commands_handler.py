from datetime import timedelta

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ChatPermissions
from aiogram.exceptions import TelegramForbiddenError

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
    mute_time = msg.text.replace("/mute", "").strip()
    if not mute_time and not mute_time.isdigit():
        mute_time = 5

    if msg.from_user.id in admins_manager.chat_admins[msg.chat.id]:
        if msg.reply_to_message:
            await msg.bot.restrict_chat_member(msg.chat.id,
                                               msg.reply_to_message.from_user.id,
                                               ChatPermissions(can_send_messages=False),
                                               until_date=timedelta(minutes=mute_time))
            await msg.bot.delete_message(msg.chat.id, msg.message_id)
        else:
            await you_have_to_answer(msg)
    else:
        await u_r_not_admin(msg)


@commands_router.message(Command(commands='report'))
async def report_user(msg: Message, admins_manager: AdminsManager):
    if msg.reply_to_message:
        for admin_id in admins_manager.chat_admins[msg.chat.id]:
            try:
                await msg.bot.forward_message(admin_id, msg.chat.id, msg.reply_to_message.message_id)
            except TelegramForbiddenError:
                print(f"bot was blocked by the admin with id {admin_id}")
    else:
        await you_have_to_answer(msg)


# TODO написать старт для админов и юзверей
@commands_router.message(Command(commands='start'))
async def start_command(msg: Message, admins_manager: AdminsManager):
    pass
