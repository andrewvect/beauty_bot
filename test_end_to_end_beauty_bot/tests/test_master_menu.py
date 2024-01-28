
import time

from base import BaseTestSetUp
from fixtures.data_to_add import add_test_data_to_db


class TestMasterPanel(BaseTestSetUp):

    def master_mailing_as_master_menu(self):
        add_test_data_to_db(self.session)

        with self.client:
            # log as admin to menu
            chat = self.client.get_chat(self.bot_name_to_test)

            message_to_log_as_admin = '/login key1'
            self.client.send_message(self.bot_name_to_test, message_to_log_as_admin)
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Личный кабинет мастера 🧑:')

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "mailing", timeout=1)
            except TimeoutError:
                pass

    def test_master_mailing_engine_without_photo(self):
        self.master_mailing_as_master_menu()
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "mailing_without_photo", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            time.sleep(1)

            self.assertEqual(last_response.text, 'Пришлите описание для рассылки')

        self.proceed_next_similar_steps()

    def test_master_mailing_engine_with_photo(self):
        self.master_mailing_as_master_menu()
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "mailing_with_photo", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            time.sleep(1)

            self.assertEqual(last_response.text, 'Пришлите фото для рассылки')

            photo_path = 'photos/1.jpg'

            self.client.send_photo(chat_id=self.bot_name_to_test, photo=photo_path)

            time.sleep(1)

        self.proceed_next_similar_steps()

    def proceed_next_similar_steps(self):
        with self.client:

            chat = self.client.get_chat(self.bot_name_to_test)

            mailing_text = 'Это описание для рассылки'

            self.client.send_message(self.bot_name_to_test, mailing_text)

            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Управление рассылкой')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "start_mailing", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Личный кабинет мастера 🧑:')






