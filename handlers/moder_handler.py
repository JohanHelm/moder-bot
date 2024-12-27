import asyncio

from aiogram import F, Router
from aiogram.types import Message

from filters.custom_filters import MeAdminFilter
from utils.curse_censor import Censorship
from utils.message_generator import notify_chat_admins_on_curse
from utils.chats_admins import AdminsManager


moder_router = Router()


@moder_router.message(F.content_type == "text", MeAdminFilter())
async def moderate_swear(msg: Message, admins_manager: AdminsManager):
    flag = await Censorship.main_filter(msg.text)

    if flag >= float(0.34):
        response = await msg.answer(f'Вы написали нецензурное слово @{msg.from_user.username}')
        await notify_chat_admins_on_curse(admins_manager, msg)
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, response.message_id)
