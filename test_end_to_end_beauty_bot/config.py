import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

DOTENV = os.path.join(os.path.dirname(__file__), "test_configuration.env")


class TestConfig(BaseSettings):

    bot_name_tg: str
    api_id: str
    api_hash: str

    model_config = SettingsConfigDict(env_file=DOTENV)
    main_script_path: Path = Path(__file__).parent.parent / "app/telegram_handlers.py"
    test_db_path: Path = Path(__file__).parent.parent / "beauty_bot1.db"


TEST_CONFIG = TestConfig()