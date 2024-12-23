from aiosqlite import connect


class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = None

    async def connect(self):
        self.connection = await connect(self.db_file)
        # await self._initialize_tables()

    async def get_chats_from_db(self):
        async with self.connection.cursor() as cursor:
            cursor_obj = await cursor.execute("SELECT chat_id FROM chats")
            result = await cursor_obj.fetchall()
            return result

    async def clear_admins_table(self):
        async with self.connection.cursor() as cursor:
            await cursor.execute(f"DELETE FROM admins")
        await self.connection.commit()

    async def add_chat_admin(self, chat_id: int, admin_id: int):
        async with self.connection.cursor() as cursor:
            await cursor.execute("INSERT INTO admins (chat_id, user_id) VALUES (?, ?)", (chat_id, admin_id,))
        await self.connection.commit()


    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
