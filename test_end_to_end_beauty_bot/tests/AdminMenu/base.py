import os
import subprocess
import time
import unittest
from pyrogram import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from test2 import clear_data
from beauty_bot.test_end_to_end_beauty_bot.config import TEST_CONFIG


class BaseTestSetUp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:

        try:
            cls.bot_process = subprocess.Popen(['python', TEST_CONFIG.main_script_path])
        except Exception as e:
            print("Error:", e)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls) -> None:
        # kill bot
        cls.bot_process.terminate()
        # delete db
        os.remove("beauty_bot.db")

    def setUp(self) -> None:
        self.bot_name_to_test = TEST_CONFIG.bot_name_tg
        api_id = TEST_CONFIG.api_id
        api_hash = TEST_CONFIG.api_hash
        self.client = Client('my_account', api_id, api_hash)

        engine = create_engine('sqlite:///beauty_bot.db', echo=True)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self) -> None:
        pass


class BaseTools(BaseTestSetUp):

    def send_message(self, message) -> None:
        with self.client:
            self.client.send_message(self.bot_name_to_test, message)
            time.sleep(1)

    def push_button(self, response, button_name) -> None:
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)
            try:
                self.client.request_callback_answer(chat.id, response.id, button_name, timeout=1)
            except TimeoutError:
                pass

    def get_response_from_bot(self, number_of_response=1) -> object:
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)
            responses = self.client.get_chat_history(chat.id, limit=number_of_response)
            for i in range(number_of_response):
                last_response = next(responses)

            return last_response

    def send_message_to_bot_and_get_reply(self, message) -> object:
        self.send_message(message)
        return self.get_response_from_bot()
