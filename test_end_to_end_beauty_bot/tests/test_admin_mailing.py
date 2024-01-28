
import time

from base import BaseTestSetUp
from fixtures.data_to_add import add_test_data_to_db


class TestAdminPanel(BaseTestSetUp):

    def process_mailing_as_admin(self):
        add_test_data_to_db(self.session)

        with self.client:
            # log as admin to menu
            chat = self.client.get_chat(self.bot_name_to_test)

            message_to_log_as_admin = '/login 1'
            self.client.send_message(self.bot_name_to_test, message_to_log_as_admin)
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Меню админа:')

            # push button choose city

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "admin_mailing", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Выберите тип рассылки:')

    def test_mailing_without_photo(self):
        self.process_mailing_as_admin()
        with self.client:
            # send City name

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_wiout_photo", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Пришлите описание для рассылки')

            mailing_text = 'Это описание для рассылки'

            self.client.send_message(self.bot_name_to_test, mailing_text)

            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Выберите город для рассылки')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_ccity1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Выберите район для рассылки')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_dist_area1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Управление рассылкой')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "start_ml_ad", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Рассылка запущена')

    def test_mailing_with_photo(self):
        self.process_mailing_as_admin()
        with self.client:
            # send City name

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_w_photo", timeout=1)
            except TimeoutError:
                pass

            photo_path = 'photos/1.jpg'

            self.client.send_photo(chat_id=self.bot_name_to_test, photo=photo_path)

            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Пришлите описание для рассылки')

            mailing_text = 'Это описание для рассылки'

            self.client.send_message(self.bot_name_to_test, mailing_text)

            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Выберите город для рассылки')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_ccity1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Выберите район для рассылки')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "ad_ml_dist_area1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Управление рассылкой')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "start_ml_ad", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Рассылка запущена')


