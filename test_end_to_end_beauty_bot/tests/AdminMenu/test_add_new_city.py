import time

from base import BaseTools


class TestAdminPanel(BaseTools):

    def process_add_new_city_as_admin(self):

        response_from_bot = self.send_message_to_bot_and_get_reply('/login 1')

        self.assertEqual(response_from_bot.text, 'Меню админа:')

        self.push_button(response_from_bot, "button2")

        self.assertEqual(self.get_response_from_bot().text, 'Напишите название города:')

    def test_add_new_city(self):
        self.process_add_new_city_as_admin()

        self.send_message('Ярославль')

        reply1 = self.get_response_from_bot(1)
        reply2 = self.get_response_from_bot(2)

        self.assertEqual(reply1.text, 'Меню админа')
        self.assertEqual(reply2.text, 'Город "Ярославль" успешно создан')

        self.push_button(reply1, "logout")

    def test_cant_add_same_city(self):
        self.process_add_new_city_as_admin()

        self.send_message('Ярославль')

        reply1 = self.get_response_from_bot(1)
        reply2 = self.get_response_from_bot(2)

        self.assertEqual(reply1.text, 'Меню админа')
        self.assertEqual(reply2.text, 'Данный город уже существует')

        self.push_button(reply1, "logout")

