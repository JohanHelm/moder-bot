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
                    self.chats_me_admin.append(chat_id)
                self.chat_admins[chat_id] = self.chat_admins.get(chat_id, [])
                if not admin.user.is_bot:
                    self.chat_admins[chat_id].append(admin_id)

    # async def save_fresh_admins_to_db(self):
    #     for chat_id in self.chat_admins.keys():
    #         for admin_id in self.chat_admins[chat_id]:
    #             await self.db.add_chat_admin(chat_id, admin_id)

    async def update_admins(self):
        await self.db.connect()
        # await self.db.clear_admins_table()
        await self.get_my_id()
        await self.get_chats_from_db()
        await self.refresh_chats_admins()
        # await self.save_fresh_admins_to_db()
        await self.db.close()

    async def add_new_admin(self, chat_id: int, new_admin_id: int):
        if new_admin_id == self.my_id:
            self.chats_me_admin.append(chat_id)
        else:
            self.chat_admins[chat_id].append(new_admin_id)

    async def from_admin_to_user(self, chat_id: int, admin_id: int):
        if admin_id == self.my_id:
            self.chats_me_admin.remove(chat_id)
        else:
            if chat_id in self.chat_admins and admin_id in self.chat_admins[chat_id]:
                self.chat_admins[chat_id].remove(admin_id)

    async def add_new_user(self, user_id, is_bot, first_name, last_name, username):
        await self.db.connect()
        await self.db.add_user_to_db(user_id, is_bot, first_name, last_name, username)
        await self.db.close()

# TODO Бота добавили в новый группу
# TODO Запись чата в БД, запись всех админов группы в БД

# TODO Пользователь вышел из группы
# TODO Отметить об уходе в БД?


