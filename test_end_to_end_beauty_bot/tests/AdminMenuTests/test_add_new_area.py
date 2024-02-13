import time

from base import BaseTools
from beauty_bot.app.tests.fixtures import add_test_data_to_db


class TestAdminPanelToAddNewArea(BaseTools):

    def process_add_new_area_as_admin(self):
        add_test_data_to_db(self.session)

        response_from_bot = self.send_message_to_bot_and_get_reply('/login 1')

        self.assertEqual(response_from_bot.text, 'Меню админа:')

        self.push_button(response_from_bot, "button3")

        self.assertEqual(self.get_response_from_bot().text, 'Напишите название района города:')

    def test_add_new_district(self):
        self.process_add_new_area_as_admin()

        reply = self.send_message_to_bot_and_get_reply('Приморский')

        self.assertEqual(reply.text, 'Доступные города')

        self.push_button(reply, "town_City1")

        self.assertEqual(self.get_response_from_bot().text, 'Меню админа')
        self.assertEqual(self.get_response_from_bot(2).text, 'Район "Приморский" успешно добавлен для города "City1"')

        self.push_button(self.get_response_from_bot(), "logout")

    def test_cant_add_same_district(self):
        self.process_add_new_area_as_admin()

        reply = self.send_message_to_bot_and_get_reply('area1')

        self.assertEqual(reply.text, 'Доступные города')

        self.push_button(reply, "town_City1")

        self.assertEqual(self.get_response_from_bot().text, 'Меню админа')
        self.assertEqual(self.get_response_from_bot(2).text, 'Район "Area1" уже существует в городе "City1"')

        self.push_button(self.get_response_from_bot(), "logout")


