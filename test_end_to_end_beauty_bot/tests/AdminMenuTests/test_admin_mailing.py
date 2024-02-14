import time

from base import BaseTools
from fixtures.data_to_add import add_test_data_to_db


class TestAdminPanel(BaseTools):

    def process_mailing_as_admin(self):
        add_test_data_to_db(self.session)

        response_from_bot = self.send_message_to_bot_and_get_reply('/login 1')

        self.assertEqual(response_from_bot.text, 'Меню админа:')

        self.push_button(response_from_bot, "admin_mailing")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите тип рассылки:')

    def test_mailing_without_photo(self):
        self.process_mailing_as_admin()

        self.push_button(self.get_response_from_bot(), "ad_ml_wiout_photo")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите описание для рассылки')

        self.send_message("Это описание для рассылки")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите город для рассылки')

        self.push_button(self.get_response_from_bot(), "ad_ml_ccity1")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите район для рассылки')

        self.push_button(self.get_response_from_bot(), "ad_ml_dist_area1")

        self.assertEqual(self.get_response_from_bot().text, 'Управление рассылкой')

        self.push_button(self.get_response_from_bot(), "start_ml_ad")

        self.assertEqual(self.get_response_from_bot().text, 'Рассылка запущена')

    def test_mailing_with_photo(self):
        self.process_mailing_as_admin()

        self.push_button(self.get_response_from_bot(), "ad_ml_w_photo")

        self.send_photo_to_bot('../../photos/1.jpg')

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите описание для рассылки')

        self.send_message("Это описание для рассылки")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите город для рассылки')

        self.push_button(self.get_response_from_bot(), "ad_ml_ccity1")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите район для рассылки')

        self.push_button(self.get_response_from_bot(), "ad_ml_dist_area1")

        self.assertEqual(self.get_response_from_bot().text, 'Управление рассылкой')

        self.push_button(self.get_response_from_bot(), "start_ml_ad")

        self.assertEqual(self.get_response_from_bot().text, 'Рассылка запущена')
