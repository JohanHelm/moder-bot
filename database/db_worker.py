from aiosqlite import connect


class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = None

    async def connect(self):
        self.connection = await connect(self.db_file)
        await self._initialize_tables()

    async def _initialize_tables(self):
        await self.connection.execute('''
               CREATE TABLE IF NOT EXISTS chats (
                   chat_id INTEGER NOT NULL,
                   chat_type REFERENCES chat_type (chat_type_id),
                   chat_title TEXT,
                   chat_username TEXT,
                   CONSTRAINT chats_pk PRIMARY KEY (chat_id)
               )
           ''')

        await self.connection.execute('''
               CREATE TABLE IF NOT EXISTS users (
                   user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                   is_bot INTEGER DEFAULT 0,
                   first_name TEXT,
                   last_name TEXT,
                   username TEXT
               )
           ''')

        await self.connection.execute('''
               CREATE TABLE IF NOT EXISTS chat_type (
                   chat_type_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   type TEXT NOT NULL
               )
           ''')

        await self.connection.execute('''
               CREATE TABLE IF NOT EXISTS admins (
                   chat_id INTEGER REFERENCES chats (chat_id),
                   user_id INTEGER REFERENCES users (user_id),
                   UNIQUE(chat_id, user_id)
               )
           ''')

        await self.connection.commit()

    async def get_chats_from_db(self):
        async with self.connection.cursor() as cursor:
            cursor_obj = await cursor.execute("SELECT chat_id FROM chats")
            result = await cursor_obj.fetchall()
            return result

    # async def clear_admins_table(self):
    #     async with self.connection.cursor() as cursor:
    #         await cursor.execute(f"DELETE FROM admins")
    #     await self.connection.commit()

    # async def add_chat_admin(self, chat_id: int, admin_id: int):
    #     async with self.connection.cursor() as cursor:
    #         await cursor.execute("INSERT INTO admins (chat_id, user_id) VALUES (?, ?)", (chat_id, admin_id,))
    #     await self.connection.commit()

    async def add_chat_to_db(self, chat_id: int, chat_type: str, chat_title: str, chat_username: str):
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT OR IGNORE INTO chats (chat_id, chat_type, chat_title, chat_username) VALUES (?, ?, ?, ?)",
                (chat_id, chat_type, chat_title, chat_username,))
        await self.connection.commit()


    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None


    async def add_user_to_db(self, user_id, is_bot, first_name, last_name, username):
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, is_bot, first_name, last_name, username) VALUES (?, ?, ?, ?, ?)",
                (user_id, is_bot, first_name, last_name, username,))
        await self.connection.commit()


    async def get_chats_for_chat_admins_from_db(self):
        async with self.connection.cursor() as cursor:
            cursor_obj = await cursor.execute("SELECT * FROM admins_chats")
            result = await cursor_obj.fetchall()
            return result

