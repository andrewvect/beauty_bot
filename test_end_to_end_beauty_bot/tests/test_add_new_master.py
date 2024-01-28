
import time

from base import BaseTestSetUp
from fixtures.data_to_add import add_test_data_to_db


class TestAdminPanel(BaseTestSetUp):

    def process_add_new_master_or_partner(self):
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
                self.client.request_callback_answer(chat.id, last_response.id, "type_", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Выберите тип анкеты')

    def process_add_new(self):

        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Пришлите имя мастера/партнера')

            self.client.send_message(self.bot_name_to_test, "Мария")
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Пришлите фото для анкеты мастера')

            photo_path = 'photos/1.jpg'

            self.client.send_photo(chat_id=self.bot_name_to_test, photo=photo_path)
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            time.sleep(1)
            self.assertEqual(last_response.text, 'Отправьте телеграмм ссылку на анкету в виде @telgram_username')

            self.client.send_message(self.bot_name_to_test, "@test_master")
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Пришлите ссылку на отзывы анкеты')

            self.client.send_message(self.bot_name_to_test, "reviews.ru")
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Пришлите ссылку на портфолио анкеты')

            self.client.send_message(self.bot_name_to_test, "portfolio.ru")
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Пришлите описание анкеты')

            self.client.send_message(self.bot_name_to_test, "Это описание анкеты")
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Доступные города')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "save_new_master_town_city1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Доступные районы выбраного города')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "save_new_master_area_area1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)
            self.assertEqual(last_response.text, 'Меню админа')

    def test_can_add_new_master(self):
        self.process_add_new_master_or_partner()
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "chose_type_master", timeout=1)
            except TimeoutError:
                pass
        self.process_add_new()

    def test_can_add_new_partner(self):
        self.process_add_new_master_or_partner()
        with self.client:
            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "chose_type_partner", timeout=1)
            except TimeoutError:
                pass

        self.process_add_new()


