from telebot import types
from telebot.types import InlineKeyboardButton

from db_queries import get_all_cities, get_all_areas_by_city_name


def keyboard_with_towns():
    keyboard = types.InlineKeyboardMarkup()

    all_cities = get_all_cities()

    for city in all_cities:
        button = types.InlineKeyboardButton(text=city.capitalize(), callback_data=f"town_{city}")
        keyboard.add(button)

    return keyboard


def keyboard_with_cities_to_find_masters_profile():
    keyboard = types.InlineKeyboardMarkup()

    all_cities = get_all_cities()

    for city in all_cities:
        button = types.InlineKeyboardButton(text=city, callback_data=f"fM_{city}")
        keyboard.add(button)

    return keyboard


def keyboard_with_cities_to_find_partners_profile():
    keyboard = types.InlineKeyboardMarkup()

    all_cities = get_all_cities()

    for city in all_cities:
        button = types.InlineKeyboardButton(text=city, callback_data=f"fP_{city}")
        keyboard.add(button)

    return keyboard


def keyboard_with_areas_to_save_new_master(city_name):
    keyboard = types.InlineKeyboardMarkup()
    count = 'save_new_master_area_'
    all_areas = get_all_areas_by_city_name(city_name[len(count):])

    for area in all_areas:
        button = types.InlineKeyboardButton(text=area, callback_data=f"save_new_master_area_{area}")
        keyboard.add(button)

    return keyboard


def keyboard_with_towns_to_save_new_master():
    keyboard = types.InlineKeyboardMarkup()
    all_cities = get_all_cities()

    for city in all_cities:
        button = types.InlineKeyboardButton(text=city, callback_data=f"save_new_master_town_{city}")
        keyboard.add(button)

    return keyboard


def admin_keyboard2():
    inline_btn_1 = InlineKeyboardButton('Создать Анкету', callback_data='type_')
    inline_btn_2 = InlineKeyboardButton('Добавить город', callback_data='button2')
    inline_btn_3 = InlineKeyboardButton('Добавить район', callback_data='button3')
    inline_btn_4 = InlineKeyboardButton('Анкеты партнеров', callback_data='partners_questionnaires')
    inline_btn_5 = InlineKeyboardButton('Анкеты мастеров', callback_data='masters_questionnaires')
    inline_btn_6 = InlineKeyboardButton('Выйти', callback_data='logout')

    inline_full = types.InlineKeyboardMarkup()
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    inline_full.add(inline_btn_3)
    inline_full.add(inline_btn_4)
    inline_full.add(inline_btn_5)
    inline_full.add(inline_btn_6)

    return inline_full


def keyboard_with_master_types():
    inline_btn_1 = InlineKeyboardButton('Мастер', callback_data='chose_type_master')
    inline_btn_2 = InlineKeyboardButton('Партнер', callback_data='chose_type_partner')

    inline_full = types.InlineKeyboardMarkup()
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    return inline_full


def menu_with_questionaries(is_active, counter, type, master_id):
    active_status = '✅'
    if is_active is False:
        active_status = '❌'

    code = None
    if type == 'masters':
        code = 'M'
    if type == 'partners':
        code = 'P'
    print(f'acv_{code}{master_id}')

    inline_btn_1 = InlineKeyboardButton(f'Статус анкеты {active_status}', callback_data=f'acv_{code}{master_id}')
    inline_btn_2 = InlineKeyboardButton('Поиск', callback_data=f'search_as_admin{code}')
    inline_btn_3 = InlineKeyboardButton('На главную', callback_data='back_menu')

    row2 = [types.InlineKeyboardButton('⏪', callback_data=f'ad_previous_page_{type}'),
            types.InlineKeyboardButton(f'{counter}', callback_data='__'),
            types.InlineKeyboardButton('⏩', callback_data=f'ad_next_page_{type}')]

    inline_full = types.InlineKeyboardMarkup(row_width=3)
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    inline_full.add(inline_btn_3)
    inline_full.add(*row2)

    return inline_full


def keyboard_with_towns_to_search():
    keyboard = types.InlineKeyboardMarkup()

    all_cities = get_all_cities()

    for city in all_cities:
        button = types.InlineKeyboardButton(text=city, callback_data=f"town_{city}")
        keyboard.add(button)

    return keyboard


def keyboard_master_menu():
    inline_btn_1 = InlineKeyboardButton('Рассылка', callback_data='mailing')
    inline_btn_2 = InlineKeyboardButton('Выйти', callback_data='out_as_ms')

    inline_full = types.InlineKeyboardMarkup()
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)

    return inline_full


def keyboard_with_mailing_type():
    inline_btn_1 = InlineKeyboardButton('Рассылка с фото', callback_data='mailing_with_photo')
    inline_btn_2 = InlineKeyboardButton('Рассылка без фото', callback_data='mailing_without_photo')

    inline_full = types.InlineKeyboardMarkup()
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)

    return inline_full


def keyboard_to_srart_mailing():
    inline_btn_1 = InlineKeyboardButton('Запустить', callback_data='start_mailing')
    inline_btn_2 = InlineKeyboardButton('Отменить', callback_data='return_to_master_menu')

    inline_full = types.InlineKeyboardMarkup()
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)

    return inline_full


def keyboard_with_user_menu(master_id, counter):
    inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{master_id}')
    inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                        callback_data=f'ms_port_{master_id}')
    inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{master_id}')
    inline_btn_4 = InlineKeyboardButton('Партнеры', callback_data=f'partners')

    row2 = [types.InlineKeyboardButton('⏪', callback_data=f'previous_user_menu_'),
            types.InlineKeyboardButton(f'{counter}', callback_data='__'),
            types.InlineKeyboardButton('⏩', callback_data=f'next_user_menu_')]

    inline_full = types.InlineKeyboardMarkup(row_width=3)
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    inline_full.add(inline_btn_3)
    inline_full.add(inline_btn_4)
    inline_full.add(*row2)

    return inline_full


def keyboard_with_user_partner_menu(master_id, counter):
    inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{master_id}')
    inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                        callback_data=f'ms_port_{master_id}')
    inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{master_id}')
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


def menu_with_questionaries_search_by_city(is_active, counter, type, master_id):
    active_status = '✅'
    if is_active is False:
        active_status = '❌'

    if type == 'masters':
        code = 'M'
    else:
        code = 'P'

    inline_btn_1 = InlineKeyboardButton(f'Статус анкеты {active_status}', callback_data=f'acvF_{code}{master_id}')
    inline_btn_2 = InlineKeyboardButton('Поиск', callback_data=f'search_as_admin{code}')
    inline_btn_3 = InlineKeyboardButton('На главную', callback_data='back_menu')

    row2 = [types.InlineKeyboardButton('⏪', callback_data=f'ad_f_previous_{type}'),
            types.InlineKeyboardButton(f'{counter}', callback_data='__'),
            types.InlineKeyboardButton('⏩', callback_data=f'ad_f_next_{type}')]

    inline_full = types.InlineKeyboardMarkup(row_width=3)
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    inline_full.add(inline_btn_3)
    inline_full.add(*row2)

    return inline_full


def keyboard_with_master(master_id):
    inline_btn_1 = InlineKeyboardButton('Записаться', callback_data=f'ms_cont_{master_id}')
    inline_btn_2 = InlineKeyboardButton('Работы мастера',
                                        callback_data=f'ms_port_{master_id}')
    inline_btn_3 = InlineKeyboardButton('Отзывы', callback_data=f'ms_reviews_{master_id}')

    inline_full = types.InlineKeyboardMarkup(row_width=3)
    inline_full.add(inline_btn_1)
    inline_full.add(inline_btn_2)
    inline_full.add(inline_btn_3)
    return inline_full