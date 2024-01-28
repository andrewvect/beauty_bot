import json
import subprocess
import time
import unittest

from pyrogram import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from test2 import clear_data


class BaseTestSetUp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        script_path = '/Users/andrey/PycharmProjects/beauty_bot_return/beauty_bot/app/telegram_handlers.py'
        cls.bot_process = subprocess.Popen(['python', script_path])
        time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.bot_process.terminate()

    def setUp(self) -> None:
        self.bot_name_to_test = '@test_beauty_kwork_bot'
        api_id = '29540942'
        api_hash = '839f0fe913ae2fd2f22cd2ed0e8cbbae'
        self.client = Client('my_account', api_id, api_hash)

        database_path = 'sqlite:///beauty_bot.db'
        engine = create_engine(database_path, echo=True)  # Set echo to True for debugging
        clear_data(engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self) -> None:
        pass



