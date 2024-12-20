from aiosqlite import connect


class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = None

    async def connect(self):
        self.connection = await connect(self.db_file)
        # await self._initialize_tables()

    # async def _initialize_tables(self):
    #     async with self.connection.cursor() as cursor:
    #         await cursor.execute(
    #             "CREATE TABLE IF NOT EXISTS chats("
    #             "chat_id INTEGER, chat_type TEXT, chat_title TEXT, chat_username TEXT)"
    #         )
    #
    #         await cursor.execute(
    #             "CREATE TABLE IF NOT EXISTS chat_type("
    #             "chat_type_id INTEGER, type TEXT)"
    #         )
    #         await cursor.execute(
    #             "CREATE TABLE IF NOT EXISTS admins("
    #             "tg_id TEXT, title TEXT, description TEXT, "
    #             "author TEXT, publishedAt DATETIME, thumbnails TEXT, "
    #             "playlist_id TEXT, channel_id TEXT, "
    #             "viewed BOOLEAN DEFAULT (0))"
    #         )
    #     await self.connection.commit()

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None




db = Database("moder_bot.db")