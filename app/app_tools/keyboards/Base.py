from telebot import types
from telebot.types import InlineKeyboardButton

from beauty_bot.app.app_tools.db_queries import db


class BaseKeyboards:

    def keyboard_mailing(self, button_mailing_with_photo, button_mailing_without_photo):
        inline_btn_1 = InlineKeyboardButton('Рассылка с фото', callback_data=button_mailing_with_photo)
        inline_btn_2 = InlineKeyboardButton('Рассылка без фото', callback_data=button_mailing_without_photo)

        inline_full = types.InlineKeyboardMarkup()
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)

        return inline_full

    def keyboard_to_start_mailing(self, button_to_start_mailing, button_to_return_to_menu):
        inline_btn_1 = InlineKeyboardButton('Запустить', callback_data=button_to_start_mailing)
        inline_btn_2 = InlineKeyboardButton('Отменить', callback_data=button_to_return_to_menu)

        inline_full = types.InlineKeyboardMarkup()
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)

        return inline_full

    def keyboard_with_cities(self, additional_parameter):
        keyboard = types.InlineKeyboardMarkup()

        all_cities = db.get_all_cities()

        for city in all_cities:
            button = types.InlineKeyboardButton(text=city.capitalize(), callback_data=f"{additional_parameter}{city}")
            keyboard.add(button)

        return keyboard

    def keyboard_with_areas(self, additional_parameter, city_name):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Все районы города', callback_data=f"{additional_parameter}_all")
        keyboard.add(button)

        count = additional_parameter
        all_areas = db.get_all_areas_by_city_name(city_name[len(count):])

        for area in all_areas:
            button = types.InlineKeyboardButton(text=area, callback_data=f"{additional_parameter}{area}")
            keyboard.add(button)

        return keyboard
