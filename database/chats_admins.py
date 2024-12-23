from aiogram import Bot
from database.db_worker import Database


class AdminsUpdater:
    def __init__(self, db_file, bot: Bot):
        self.db = Database(f"{db_file}")
        self.bot = bot

    async def get_my_id(self, bot: Bot) -> int:
        my_user_data = await bot.get_me()
        return my_user_data.id

    async def refresh_chats_admins(self, chats_ids: list):
        for chat_id in chats_ids:
            admins = await self.bot.get_chat_administrators(chat_id)
            for admin in admins:
                admin_id = admin.user.id
                await self.db.add_chat_admin(chat_id, admin_id)

    async def get_chats_from_db(self):
        chats_ids = [item[0] for item in await self.db.get_chats_from_db()]
        return chats_ids

    async def update_admins(self):
        await self.db.connect()
        await self.db.clear_admins_table()
        chats_ids =await self.get_chats_from_db()
        await self.refresh_chats_admins(chats_ids)
        await self.db.close()


class AdminsManager:
    def __init__(self, db_file, bot):
        self.db = Database(f"{db_file}")
        self.bot = bot

    async def get_my_id(self, bot: Bot) -> int:
        my_user_data = await bot.get_me()
        return my_user_data.id


#Достать из базы все чаты, просмотреть всех админов во всех чатах, обновить всех админов во всех чатах в базе
        # print(*await bot.get_chat_administrators('-1002400455551'), sep='\n')
        # my_id = await get_my_id(bot)
        # print(my_id)
# словарь с ключами это id чатов, значение это списки с id админов чата.

# Отслеживать добавление пользователя в админы, добавлять в админы в базе
# Удалять из админов в базе