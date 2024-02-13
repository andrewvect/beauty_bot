import time

from beauty_bot.test_end_to_end_beauty_bot.tests.AdminMenuTests.base import BaseTools
from fixtures.data_to_add import add_test_data_to_db


class TestMasterPanel(BaseTools):

    def master_mailing_as_master_menu(self):
        add_test_data_to_db(self.session)

        self.send_message('/login key1')

        self.assertEqual(self.get_response_from_bot().text, 'Личный кабинет мастера 🧑:')

        self.push_button(self.get_response_from_bot(), "mailing")

    def test_master_mailing_engine_without_photo(self):
        self.master_mailing_as_master_menu()

        self.push_button(self.get_response_from_bot(), "mailing_without_photo")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите описание для рассылки')

        self.proceed_next_similar_steps()

    def test_master_mailing_engine_with_photo(self):

        self.master_mailing_as_master_menu()

        self.push_button(self.get_response_from_bot(), "mailing_with_photo")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите фото для рассылки')

        self.send_photo_to_bot('../../photos/1.jpg')

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите описание для рассылки')

        self.proceed_next_similar_steps()

    def proceed_next_similar_steps(self):

        self.send_message('Это описание для рассылки')

        self.assertEqual(self.get_response_from_bot().text, 'Управление рассылкой')

        self.push_button(self.get_response_from_bot(), "start_mailing")

        self.assertEqual(self.get_response_from_bot().text, 'Личный кабинет мастера 🧑:')
