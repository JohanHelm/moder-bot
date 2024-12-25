import asyncio

from aiogram import F, Router
from aiogram.types import Message

from filters.custom_filters import MeAdminFilter
from utils.curse_censor import Censorship


moder_router = Router()


@moder_router.message(F.content_type == "text", MeAdminFilter())
async def moderate_swear(msg: Message):
    flag = await Censorship.main_filter(msg.text)

    if flag >= float(0.34):
        response = await msg.answer(f'Вы написали нецензурное слово @{msg.from_user.username}')
        await msg.bot.delete_message(msg.chat.id, msg.message_id)
        await asyncio.sleep(3)
        await msg.bot.delete_message(msg.chat.id, response.message_id)
    # print(*msg, sep='\n')