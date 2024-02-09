import time

from base import BaseTestSetUp


class TestAdminPanel(BaseTestSetUp):

    def process_add_new_city_as_admin(self):
        # add_test_data_to_db(self.session)

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
                self.client.request_callback_answer(chat.id, last_response.id, "button3", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Напишите название района города:')



    def test_add_new_district(self):
        self.process_add_new_city_as_admin()
        with self.client:
            # send City name
            message_city_name = 'Приморский'
            self.client.send_message(self.bot_name_to_test, message_city_name)
            time.sleep(1)

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Доступные города')
            time.sleep(1)

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "town_City1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)
            last_response2 = next(responses)

            self.assertEqual(last_response2.text, 'Район "Приморский" успешно добавлен для города "City1"')

    def test_cant_add_same_district(self):
        self.process_add_new_city_as_admin()
        with self.client:
            # send Area name
            message_area_name = 'Area1'
            self.client.send_message(self.bot_name_to_test, message_area_name)
            time.sleep(1)

            chat = self.client.get_chat(self.bot_name_to_test)

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)

            self.assertEqual(last_response.text, 'Доступные города')

            try:
                self.client.request_callback_answer(chat.id, last_response.id, "town_city1", timeout=1)
            except TimeoutError:
                pass

            responses = self.client.get_chat_history(chat.id, limit=2)
            last_response = next(responses)
            last_response2 = next(responses)

            self.assertEqual(last_response2.text, f'Район "{message_area_name}" уже существует в городе "City1"')
