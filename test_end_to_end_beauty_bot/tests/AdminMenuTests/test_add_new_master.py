from base import BaseTools
from fixtures.data_to_add import add_test_data_to_db


class TestAdminPanel(BaseTools):

    def process_add_new_master_or_partner(self):
        add_test_data_to_db(self.session)

        response_from_bot = self.send_message_to_bot_and_get_reply('/login 1')

        self.assertEqual(response_from_bot.text, 'Меню админа:')

        self.push_button(response_from_bot, "type_")

        self.assertEqual(self.get_response_from_bot().text, 'Выберите тип анкеты')

    def process_add_new(self):
        self.assertEqual(self.get_response_from_bot().text, 'Пришлите имя мастера/партнера')

        self.send_message('Мария')

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите фото для анкеты мастера')

        self.send_photo_to_bot('../../photos/1.jpg')

        self.assertEqual(self.get_response_from_bot().text,
                         'Отправьте телеграмм ссылку на анкету в виде @telgram_username')

        self.send_message("@test_master")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите ссылку на отзывы анкеты')

        self.send_message("reviews.ru")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите ссылку на портфолио анкеты')

        self.send_message("portfolio.ru")

        self.assertEqual(self.get_response_from_bot().text, 'Пришлите описание анкеты')

        self.send_message("Это описание анкеты")

        self.assertEqual(self.get_response_from_bot().text, 'Доступные города')

        self.push_button(self.get_response_from_bot(), "save_new_master_town_city1")

        self.assertEqual(self.get_response_from_bot().text, 'Доступные районы выбраного города')

        self.push_button(self.get_response_from_bot(), "save_new_master_area_area1")

        self.assertEqual(self.get_response_from_bot().text, 'Меню админа')

    def test_can_add_new_master(self):
        self.process_add_new_master_or_partner()
        self.push_button(self.get_response_from_bot(), "chose_type_master")
        self.process_add_new()

    def test_can_add_new_partner(self):
        self.process_add_new_master_or_partner()
        self.push_button(self.get_response_from_bot(), "chose_type_partner")
        self.process_add_new()
