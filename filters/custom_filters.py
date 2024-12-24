from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.chats_admins import AdminsManager



class MeAdminFilter(BaseFilter):

    async def __call__(self, message: Message, admins_manager: AdminsManager) -> bool:
        return message.chat.id in admins_manager.chats_me_admin

