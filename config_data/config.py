from dataclasses import dataclass
from environs import Env
from pathlib import Path

@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    # admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    # db: DatabaseConfig


def load_config(secrets_file_path: Path | None = None) -> Config:
    env: Env = Env()
    env.read_env(secrets_file_path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN')),

        # db=DatabaseConfig(
        #     database=env('DATABASE'),
        #     db_host=env('DB_HOST'),
        #     db_user=env('DB_USER'),
        #     db_password=env('DB_PASSWORD')
        # )
    )