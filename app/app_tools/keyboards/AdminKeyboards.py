from telebot import types
from telebot.types import InlineKeyboardButton

from beauty_bot.app.app_tools.keyboards.Base import BaseKeyboards
from beauty_bot.app.app_tools.keyboards.CallBackButtons import AdminCallBackButtons


class AdminKeyboards(BaseKeyboards, AdminCallBackButtons):
    def keyboard_with_mailing_as_admin(self):
        return super().keyboard_mailing(self.mailing_with_photo, self.mailing_without_photo)

    def keyboard_with_cities_for_admin_mailing(self):
        return self.keyboard_with_cities(self.button_with_cities)

    def keyboard_with_districts_for_admin_mailing(self, city_name):
        return self.keyboard_with_areas(self.button_with_districts, city_name)

    def keyboard_to_start_mailing_as_admin(self):
        return super().keyboard_to_start_mailing(self.start_mailing, self.return_to_admin_menu)

    def admin_keyboard_with_questionaries(self, menu, type):

        active_status = '✅'
        if menu.master_data['is_active'] is False:
            active_status = '❌'

        if type == 'masters':
            code = 'M'
        else:
            code = 'P'

        inline_btn_1 = InlineKeyboardButton(f'Статус анкеты {active_status}',
                                            callback_data=f'{self.change_status}{type}{menu.masted_data["id"]}')
        inline_btn_2 = InlineKeyboardButton('Поиск', callback_data=f'{self.search_button}{code}')
        inline_btn_3 = InlineKeyboardButton('На главную', callback_data={self.return_to_admin_menu})

        row2 = [types.InlineKeyboardButton('⏪', callback_data=f'{self.previous}{type}'),
                types.InlineKeyboardButton(f'{menu.count_numbers()}', callback_data='__'),
                types.InlineKeyboardButton('⏩', callback_data=f'{self.next}{type}')]

        inline_full = types.InlineKeyboardMarkup(row_width=3)
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        inline_full.add(inline_btn_3)
        inline_full.add(*row2)

        return inline_full

    def menu_with_questionaries_searched_by_city(self, menu, type):
        return self.admin_main_menu_with_questionaries(menu, type)

    def admin_main_menu_with_questionaries(self, menu, type):
        return self.admin_keyboard_with_questionaries(menu, type)

    def admin_keyboard_main_menu(self):
        inline_btn_1 = InlineKeyboardButton('Создать Анкету', callback_data=self.create_questionary)
        inline_btn_2 = InlineKeyboardButton('Добавить город', callback_data=self.add_city)
        inline_btn_3 = InlineKeyboardButton('Добавить район', callback_data=self.add_district)
        inline_btn_4 = InlineKeyboardButton('Анкеты партнеров', callback_data=self.partners_questionnaires)
        inline_btn_5 = InlineKeyboardButton('Анкеты мастеров', callback_data=self.masters_questionnaires)
        inline_btn_6 = InlineKeyboardButton('Рассылка', callback_data=self.admin_mailing)
        inline_btn_7 = InlineKeyboardButton('Выйти', callback_data=self.logout)

        inline_full = types.InlineKeyboardMarkup()
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        inline_full.add(inline_btn_3)
        inline_full.add(inline_btn_4)
        inline_full.add(inline_btn_5)
        inline_full.add(inline_btn_6)
        inline_full.add(inline_btn_7)

        return inline_full

    def keyboard_with_towns(self):
        return self.keyboard_with_cities(self.add_city2)

    def keyboard_with_cities_to_find_masters_profile(self):
        return self.keyboard_with_cities(self.find_master)

    def keyboard_with_cities_to_find_partners_profile(self):
        return self.keyboard_with_cities(self.find_partner)

    def keyboard_with_areas_to_save_new_master(self, city_name):
        return self.keyboard_with_areas(city_name, self.save_new_master_area)

    def keyboard_with_towns_to_save_new_master(self):
        return self.keyboard_with_cities(self.save_new_master_town)

    def keyboard_with_master_types(self):
        inline_btn_1 = InlineKeyboardButton('Мастер', callback_data=self.choose_master_type)
        inline_btn_2 = InlineKeyboardButton('Партнер', callback_data=self.choose_partner_type)

        inline_full = types.InlineKeyboardMarkup()
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        return inline_full


admin_keyboards = AdminKeyboards()