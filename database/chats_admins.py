from aiogram import Bot
from database.db_worker import Database



class AdminsManager:
    def __init__(self, db_file, bot: Bot):
        self.db = Database(f"{db_file}")
        self.bot = bot
        self.my_id = None
        self.chats_ids = None
        self.chats_me_admin = []
        self.chat_admins = {}

    async def get_my_id(self):
        my_user_data = await self.bot.get_me()
        self.my_id = my_user_data.id

    async def get_chats_from_db(self):
        self.chats_ids = [item[0] for item in await self.db.get_chats_from_db()]

    async def refresh_chats_admins(self):
        for chat_id in self.chats_ids:
            admins = await self.bot.get_chat_administrators(chat_id)
            for admin in admins:
                admin_id = admin.user.id
                if admin_id == self.my_id:
                    self.chats_me_admin.append(admin_id)
                self.chat_admins[chat_id] = self.chat_admins.get(chat_id, [])
                self.chat_admins[chat_id].append(admin_id)

    async def save_fresh_admins_to_db(self):
        for chat_id in self.chat_admins.keys():
            for admin_id in self.chat_admins[chat_id]:
                await self.db.add_chat_admin(chat_id, admin_id)

    async def update_admins(self):
        await self.db.connect()
        await self.db.clear_admins_table()
        await self.get_my_id()
        await self.get_chats_from_db()
        await self.refresh_chats_admins()
        await self.save_fresh_admins_to_db()
        await self.db.close()


# class AdminsManager:
#     def __init__(self, db_file, bot):
#         self.db = Database(f"{db_file}")
#         self.bot = bot
#
#     async def get_my_id(self, bot: Bot) -> int:
#         my_user_data = await bot.get_me()
#         return my_user_data.id


#Достать из базы все чаты, просмотреть всех админов во всех чатах, обновить всех админов во всех чатах в базе
        # print(*await bot.get_chat_administrators('-1002400455551'), sep='\n')
        # my_id = await get_my_id(bot)
        # print(my_id)
# словарь с ключами это id чатов, значение это списки с id админов чата.

# Отслеживать добавление пользователя в админы, добавлять в админы в базе
# Удалять из админов в базе