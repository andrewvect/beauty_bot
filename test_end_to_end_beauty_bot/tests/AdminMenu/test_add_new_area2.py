import time

from base import BaseTestSetUp


class TestAdminPanel(BaseTestSetUp):

    def send_message_with_assert(self, message, expected_response):
        chat = self.client.get_chat(self.bot_name_to_test)
        with self.client:
            self.client.send_message(self.bot_name_to_test, message)
            time.sleep(1)

            responses = self.client.get_chat_history(chat.id, limit=1)
            last_response = next(responses)

            self.assertEqual(last_response.text, expected_response)

            return last_response

    def push_button_and_pass_timeout(self, button_name, last_response):
        chat = self.client.get_chat(self.bot_name_to_test)
        with self.client:
            try:
                self.client.request_callback_answer(chat.id, last_response.id, button_name, timeout=1)
            except TimeoutError:
                pass

    def assert_last_response(self, expected_response):
        chat = self.client.get_chat(self.bot_name_to_test)
        responses = self.client.get_chat_history(chat.id, limit=1)
        last_response = next(responses)
        self.assertEqual(last_response.text, expected_response)
        return last_response

    def process_add_new_city_as_admin(self):

        last_response = self.send_message_with_assert('/login 1', 'Меню админа:')

        self.push_button_and_pass_timeout("button3", last_response)

        self.assert_last_response('Напишите название района города:')

    def test_add_new_district(self):
        self.process_add_new_city_as_admin()

        last_response = self.send_message_with_assert('Приморский', 'Доступные города')

        self.push_button_and_pass_timeout("town_City1", last_response)

        self.assert_last_response('Район "Приморский" успешно добавлен для города "City1"')


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
