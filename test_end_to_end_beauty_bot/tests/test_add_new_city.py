
import time

from base import BaseTestSetUp


class TestAdminPanel(BaseTestSetUp):

    def process_add_new_city_as_admin(self):
        with self.client:
            # log as admin to menu
            chat = self.client.get_chat(self.bot_name_to_test)

            message_to_log_as_admin = '/login 1'
            self.client.send_message(self.bot_name_to_test, message_to_log_as_admin)
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Меню админа:')

            # push button "Добавить город"

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "button2", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Напишите название города:')

    def test_add_new_city(self):
        self.process_add_new_city_as_admin()
        with self.client:
            # send City name
            message_city_name = 'Ярославль'
            self.client.send_message(self.bot_name_to_test, message_city_name)
            time.sleep(1)

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)
            last_response2 = next(responses)

            self.assertEqual(last_response2.text, 'Город "Ярославль" успешно создан')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "logout", timeout=1)
            except TimeoutError:
                pass

    def test_cant_add_same_city(self):
        self.process_add_new_city_as_admin()
        with self.client:
            # send City name
            message_city_name = 'Ярославль'
            self.client.send_message(self.bot_name_to_test, message_city_name)
            time.sleep(1)

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)
            last_response2 = next(responses)

            self.assertEqual(last_response2.text, 'Данный город уже существует')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "logout", timeout=1)
            except TimeoutError:
                pass

