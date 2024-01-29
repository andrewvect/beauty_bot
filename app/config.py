import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class AppConfig(BaseSettings):
    admin_key: str
    bot_key: str
    bot_name_tg: str

    model_config = SettingsConfigDict(env_file=DOTENV)


CONFIG = AppConfig()

# Logging.
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

handler = logger.handlers and logger.handlers[0] or logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s [%(filename)s:%(lineno)s] %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

