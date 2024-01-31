import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), "test_configuration.env")


class TestConfig(BaseSettings):

    bot_name_tg: str
    api_id: str
    api_hash: str

    model_config = SettingsConfigDict(env_file=DOTENV)


TEST_CONFIG = TestConfig()