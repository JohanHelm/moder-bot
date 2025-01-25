from aiogram import Bot
from database.db_worker import Database


class MeTgBot:
    def __init__(self, bot: Bot):
        self.my_own_id = self.get_my_id(bot)
        self.chat_ids_me_in = []
        self.chat_ids_me_admin = []

    async def get_my_id(self, bot: Bot):
        my_user_data = await bot.get_me()
        self.my_own_id = my_user_data.id


class TgChat:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.chat_rules_tg_msg_link: str = ""
        self.chat_admins = []
        self.chat_for_chat_admins = []

    async def add_chat_rules_tg_msg_link(self):
        pass

    async def add_chat_for_chat_admins(self):
        pass


class MainManager:
    def __init__(self, db_file, bot: Bot):
        self.db = Database(f"{db_file}")
        self.bot = bot
        self.me_tg_bot = MeTgBot(bot)
        self.chats_list = []

    async def get_chats_from_db(self) -> list[int]:
        chats_ids = [item[0] for item in await self.db.get_chats_from_db()]
        return chats_ids

    async def create_tg_chats(self, chats_ids: list[int]):
        for chat_id in chats_ids:
            self.chats_list.append(await self.create_tg_chat(chat_id))

    async def create_tg_chat(self, chat_id: int) -> TgChat:
        tg_chat = TgChat(chat_id)
        chat_admins = await self.bot.get_chat_administrators(chat_id)
        for admin in chat_admins:
            admin_id = admin.user.id
            if admin_id == self.me_tg_bot.my_own_id:
                self.me_tg_bot.chat_ids_me_admin.append(chat_id)
            if not admin.user.is_bot:
                tg_chat.chat_admins.append(admin_id)
        return tg_chat


    async def init_main_manager(self):
        await self.db.connect()
        chats_ids = await self.get_chats_from_db()
        await self.create_tg_chats(chats_ids)
        await self.db.close()


class AdminsManager:
    def __init__(self, db_file, bot: Bot):
        self.db = Database(f"{db_file}")
        self.bot = bot
        self.my_id = None
        self.chats_ids = None
        self.chats_me_admin = []
        self.chat_admins = {}
        self.chats_for_chat_admins = {}

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

    async def refresh_chats_for_chat_admins(self):
        chats_for_chat_admins = await self.db.get_chats_for_chat_admins_from_db()
        self.chats_for_chat_admins = dict(chats_for_chat_admins)


    async def update_admins(self):
        await self.db.connect()
        await self.get_my_id()
        await self.get_chats_from_db()
        await self.refresh_chats_admins()
        await self.refresh_chats_for_chat_admins()
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


