from beauty_bot.app.app_tools.keyboards.Base import BaseKeyboards

from telebot import types
from telebot.types import InlineKeyboardButton


class UserKeyboards(BaseKeyboards):

    def keyboard_with_user_main_menu(self, master_id):
        inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{master_id}')
        inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                            callback_data=f'ms_port_{master_id}')
        inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{master_id}')

        inline_full = types.InlineKeyboardMarkup(row_width=3)
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        inline_full.add(inline_btn_3)
        return inline_full

    def keyboard_with_profile_by_type(self, type, menu):
        pass

    def keyboard_with_user_partner_menu(self, master_id, counter, url_to_reviews, url_to_works, url_to_partner):
        inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{master_id}',
                                            url='t.me/' + url_to_partner[1:])
        inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                            callback_data=f'ms_port_{master_id}', url=url_to_works)
        inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{master_id}', url=url_to_reviews)
        inline_btn_4 = InlineKeyboardButton('Назад', callback_data='back_us_menu')

        row2 = [types.InlineKeyboardButton('⏪', callback_data=f'previous_partn_menu_'),
                types.InlineKeyboardButton(f'{counter}', callback_data='__'),
                types.InlineKeyboardButton('⏩', callback_data=f'next_partn_menu_')]

        inline_full = types.InlineKeyboardMarkup(row_width=3)
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        inline_full.add(inline_btn_3)
        inline_full.add(inline_btn_4)
        inline_full.add(*row2)

        return inline_full

    def keyboard_with_user_menu(self, menu):
        inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{menu.master_data["id"]}',
                                            url='t.me/' + menu.master_data['telegram_user_name'][1:])
        inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                            callback_data=f'ms_port_{menu.master_data["id"]}',
                                            url=menu.master_data['master_portfolio_url'])
        inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{menu.master_data["id"]}',
                                            url=menu.master_data['reviews_url'])
        inline_btn_4 = InlineKeyboardButton('Партнеры', callback_data=f'partners_mn_{menu.master_data["location_id"]}')

        row2 = [types.InlineKeyboardButton('⏪', callback_data=f'previous_user_menu_'),
                types.InlineKeyboardButton(f'{menu.count_numbers()}', callback_data='__'),
                types.InlineKeyboardButton('⏩', callback_data=f'next_user_menu_')]

        inline_full = types.InlineKeyboardMarkup(row_width=3)
        inline_full.add(inline_btn_1)
        inline_full.add(inline_btn_2)
        inline_full.add(inline_btn_3)
        inline_full.add(inline_btn_4)
        inline_full.add(*row2)

        return inline_full


user_keyboards = UserKeyboards()
