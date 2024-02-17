import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class AppConfig(BaseSettings):
    admin_key: str
    bot_key: str
    bot_name_tg: str

    model_config = SettingsConfigDict(env_file=DOTENV)


CONFIG = AppConfig()


