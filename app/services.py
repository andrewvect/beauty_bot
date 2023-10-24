import string
import random
import traceback

from keyboards import keyboard_with_areas_to_save_new_master, keyboard_with_towns_to_save_new_master, \
    keyboard_with_towns, admin_keyboard2, menu_with_questionaries, keyboard_with_mailing_type, keyboard_master_menu, \
    keyboard_to_srart_mailing, keyboard_with_user_menu, keyboard_with_user_partner_menu, keyboard_with_master
from logger import log_error
from db_queries import add_new_city, add_new_area, get_city_id_by_name, \
    add_new_master, get_partners_questionaries_for_admin_menu, get_area_id_by_name, \
    get_masters_questionaries_for_admin_menu, get_all_master_subscribers_by_master_telegram_username, \
    get_key_by_telegram_username, \
    subscribe_user_on_master, get_master_photo_name_by_telegram_username, get_masters_profiles_for_user_menu, \
    get_master_telegram_url_by_id, get_master_portfolio_url_by_id, \
    get_master_reviews_url_by_id, get_all_master_subscribe_profiles, get_all_partner_subscribe_profiles, \
    set_master_active_profile, get_all_masters_id_by_name_city, get_masters_questionaries_for_admin_menu_by_city, \
    get_partners_questionaries_for_admin_menu_by_city, get_master_id_by_ref_url, get_questionary_for_user_menu_by_id, \
    check_if_city_exist, check_if_area_exist
from keyboards import keyboard_with_master_types
from extantions import bot
from config import bot_name_tg
import secrets

selected_area = ''


def generate_10_digit_key():
    key = ''.join(secrets.choice('0123456789') for _ in range(10))
    return key


def generate_key(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def is_login_command(message):
    split_str = message.text.lower().split()
    if split_str[0] == '/login' and len(split_str) == 2:
        return True
    else:
        return False


def admin_logout(call):
    bot.delete_message(call.message.chat.id, call.message.id)


# save new master questionnaire

new_master_state = {}


def process_choose_type_master(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, "Выберите тип анкеты", reply_markup=keyboard_with_master_types())


def handle_master_type_click(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)

        count = len('chose_type_')
        if call.data[count:] == 'partner':
            new_master_state['is_partner'] = True
        else:
            new_master_state['is_partner'] = False

        bot.send_message(call.message.chat.id, "Пришлите имя мастера/партнера")

        bot.register_next_step_handler(call.message, process_new_master_username_step)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_new_master_username_step(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

        new_master_state['username'] = message.text

        bot.send_message(message.chat.id, "Пришлите фото для анкеты мастера")
        bot.register_next_step_handler(message, process_new_master_photo_step)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_new_master_photo_step(message):
    try:
        bot.delete_message(message.chat.id, message.id - 1)
        bot.delete_message(message.chat.id, message.id)

        photo = message.photo[-1]
        file_id = photo.file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        file_name = generate_key(7)

        with open(f'photos/{file_name}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        new_master_state['file_name'] = file_name

        bot.send_message(message.chat.id, "Отправьте телеграмм ссылку на анкету в виде @telgram_username")
        bot.register_next_step_handler(message, process_master_telegram_id)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_master_telegram_id(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

        new_master_state['telegram_username'] = message.text

        bot.send_message(message.chat.id, "Пришлите ссылку на отзывы анкеты")
        bot.register_next_step_handler(message, process_master_reviews_url)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_master_reviews_url(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

        new_master_state['reviews_url'] = message.text

        bot.send_message(message.chat.id, "Пришлите ссылку на портфолио анкеты")
        bot.register_next_step_handler(message, process_portfolio_url)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_portfolio_url(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

        new_master_state['portfolio_url'] = message.text

        bot.send_message(message.chat.id, "Пришлите описание анкеты")
        bot.register_next_step_handler(message, process_new_master_description)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_new_master_description(message):
    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    new_master_state['description'] = message.text

    bot.send_message(message.chat.id, "Выберите город для анкеты")
    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns_to_save_new_master())


def handle_save_new_master_town(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    new_master_state['town'] = call.data

    bot.send_message(call.message.chat.id, "Выберите район для мастера")
    bot.send_message(call.message.chat.id, "Доступные районы выбраного города",
                     reply_markup=keyboard_with_areas_to_save_new_master(call.data))


def handle_save_new_master(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    new_master_state['area'] = call.data[len('save_new_master_area_'):]
    area_id = get_area_id_by_name(new_master_state['area'])

    api_key = generate_key(10)
    referal_key = generate_key(10)

    add_new_master(new_master_state['telegram_username'],
                   api_key,
                   referal_key,
                   new_master_state['description'],
                   new_master_state['username'],
                   new_master_state['file_name'],
                   new_master_state['is_partner'],
                   True,
                   area_id,
                   new_master_state['reviews_url'],
                   new_master_state['portfolio_url']
                   )

    value = 'мастера'
    if new_master_state['is_partner']:
        value = 'партнера'

    bot.send_message(call.message.chat.id, f"Анкета {value} {new_master_state['username']} создана!\n"
                                           f"Api key: {api_key} \n"
                                           f"Referal link: https://t.me/{bot_name_tg}?start={referal_key}")
    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


"""
show quastionaries as admin
"""

masters_page_questionare = 1
partners_page_questionare = 1
all_questionaries = 0


def send_menu_with_masters(call):
    send_menu_with_questionaries(call, 'masters')


def send_menu_with_partners(call):
    send_menu_with_questionaries(call, 'partners')


def send_menu_with_questionaries(call, type):
    try:
        try:
            bot.delete_message(call.message.chat.id, call.message.id)

        except Exception:
            pass

        data = None
        page_numbers = None

        if type == 'masters':
            data = get_masters_questionaries_for_admin_menu(masters_page_questionare)
            page_numbers = f"{masters_page_questionare}/{data['page_counter']}"
        if type == 'partners':
            data = get_partners_questionaries_for_admin_menu(partners_page_questionare)
            page_numbers = f"{partners_page_questionare}/{data['page_counter']}"

        message = f"{data['questionary']['description']} \n" \
                  f"Город: {data['questionary']['city_name'].capitalize()} \n" \
                  f"Район города: {data['questionary']['area_name'].capitalize()} \n"

        global all_questionaries
        all_questionaries = data['page_counter']

        with open(f"photos/{data['questionary']['url_to_photo']}.jpg", 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)

        bot.send_message(call.message.chat.id, message,
                         reply_markup=menu_with_questionaries(data['questionary']['is_active'],
                                                              page_numbers, type, data['questionary']['master_id']))

    except Exception:
        bot.send_message(call.message.chat.id, "Не создано еще ни одной анкеты.")
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


def next_page_masters_admin_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global masters_page_questionare

    if masters_page_questionare == all_questionaries:
        pass
    else:
        masters_page_questionare += 1

    send_menu_with_questionaries(call, call.data[len('ad_next_page_'):])


def previous_page_masters_admin_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global masters_page_questionare
    if masters_page_questionare == 1:
        pass
    else:
        masters_page_questionare -= 1

    send_menu_with_questionaries(call, call.data[len('ad_previous_page_'):])


def next_page_partners_admin_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global partners_page_questionare

    if partners_page_questionare == all_questionaries:
        pass
    else:
        partners_page_questionare += 1

    send_menu_with_questionaries(call, call.data[len('ad_next_page_'):])


def previous_page_partners_admin_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global partners_page_questionare
    if partners_page_questionare == 1:
        pass
    else:
        partners_page_questionare -= 1

    send_menu_with_questionaries(call, call.data[len('ad_previous_page_'):])


def process_ckeck_city(message):
    global selected_area
    selected_area = message.text.lower()

    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns())


def process_save_new_city(message):
    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    if check_if_city_exist(message.text):
        bot.send_message(message.chat.id, f'Данный город уже существует')
    else:
        bot.send_message(message.chat.id, f'Город "{message.text.capitalize()}" успешно создан')
        add_new_city(message.text)

    bot.send_message(message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


def handle_button2_click(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Напишите название города:")
        bot.register_next_step_handler(call.message, process_save_new_city)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def handle_button3_click(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Напишите название района города:")
        bot.register_next_step_handler(call.message, process_ckeck_city)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def handle_save_area_town(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    city_id = get_city_id_by_name(call.data[5:])

    if check_if_area_exist(selected_area, city_id):
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" уже существует в городе "{call.data[5:].capitalize()}"')
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
    else:
        add_new_area(city_id, selected_area)
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" успешно добавлен для города "{call.data[5:].capitalize()}"')
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


def back_to_admin_menu_from_questionaries(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    bot.send_message(call.message.chat.id, "Меню админа:", reply_markup=admin_keyboard2())


def back_to_admin_menu_create_questionary(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    bot.send_message(call.message.chat.id, "Меню админа:", reply_markup=admin_keyboard2())


def change_master_visibility(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    master_id = call.data[len('acv_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_questionaries(call, 'masters')


def change_partner_visibility(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    master_id = call.data[len('acv_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_questionaries(call, 'partners')


"""
master menu with mailing
"""
new_masters_mailing_state = dict()


def send_keyboard_with_master_menu(message):
    bot.delete_message(message.chat.id, message.id)
    bot.send_message(message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


def send_keyboard_with_mailing_type(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    new_masters_mailing_state[call.message.chat.id] = {}

    bot.send_message(call.message.chat.id, "Выберите тип рассылки:", reply_markup=keyboard_with_mailing_type())


def process_answer_for_new_mailing_with_photo(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Пришлите фото для рассылки")

        bot.register_next_step_handler(call.message, process_save_photo_for_new_mailing)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_answer_for_new_mailing_without_photo(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Пришлите описание для рассылки")

        bot.register_next_step_handler(call.message, process_save_description_for_new_mailing)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_save_photo_for_new_mailing(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)

        photo = message.photo[-1]
        file_id = photo.file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        file_name = generate_key(7)

        with open(f'photos/{file_name}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        new_masters_mailing_state[message.chat.id]['photo'] = file_name

        bot.send_message(message.chat.id, "Пришлите описание для рассылки")

        bot.register_next_step_handler(message, process_save_description_for_new_mailing)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды(")


def process_save_description_for_new_mailing(message):
    bot.delete_message(message.chat.id, message.id)

    new_masters_mailing_state[message.chat.id]['description'] = message.text

    message_text = f"{new_masters_mailing_state[message.chat.id]['description']} \n" \
                   f"Контакт: @{message.from_user.username}"

    if len(new_masters_mailing_state[message.chat.id]) == 1:
        photo_master_name = get_master_photo_name_by_telegram_username('@' + message.chat.username)
        new_masters_mailing_state[message.chat.id]['photo'] = photo_master_name

        with open(f"photos/{photo_master_name + '.jpg'}", 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=message_text)

    else:
        with open(f"photos/{new_masters_mailing_state[message.chat.id]['photo'] + '.jpg'}", 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=message_text)

    bot.send_message(message.chat.id, 'Управление рассылкой', reply_markup=keyboard_to_srart_mailing())


def start_mailing(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    subscribers_telegram_ids = get_all_master_subscribers_by_master_telegram_username(call.message.chat.username)

    if not subscribers_telegram_ids:
        bot.send_message(call.message.chat.id, "У вас еще нет подписчиков")
    else:
        bot.send_message(call.message.chat.id, "Рассылка запущена")

        for user_id in subscribers_telegram_ids:
            message_text = f"{new_masters_mailing_state[call.message.chat.id]['description']} \n" \
                           f"Контакт: @{call.message.chat.username}"

            with open(f"photos/{new_masters_mailing_state[call.message.chat.id]['photo'] + '.jpg'}", 'rb') as photo:
                bot.send_photo(user_id, photo, caption=message_text)

    bot.send_message(call.message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


# authorisation as master
def check_master_key(user_name, key):
    user_key = get_key_by_telegram_username('@' + user_name)
    if user_key.lower() == key:
        return True
    return False


# subscribe
def subscribe_on_master(user_name, ref_url):
    subscribe_user_on_master(user_name, ref_url)


# user menu
user_state = {}


def send_user_menu(message):
    try:
        bot.delete_message(message.chat.id, message.id)
        bot.delete_message(message.chat.id, message.id - 1)
    except Exception:
        pass

    if 'masters' in user_state.get(message.chat.id, {}):
        pass
    else:
        user_state[message.chat.id] = {'masters': {'page': 1, 'count_pages': 1}}

    user_masters_id = get_all_master_subscribe_profiles(message.chat.id)

    if not user_masters_id:
        bot.send_message(message.chat.id, 'Вы еще не подписались ни на один профиль')
    else:
        user_page = user_state[message.chat.id]['masters']['page']

        master_id = user_masters_id[user_page - 1]

        counter = str(user_state[message.chat.id]['masters']['page']) + '/' + str(len(user_masters_id))
        user_state[message.chat.id]['masters']['number_all_pages'] = len(user_masters_id)

        data_profile = get_masters_profiles_for_user_menu(master_id)
        message_text = f"{data_profile['username']} \n" \
                       f"{data_profile['description']} \n" \
                       f"Город: {data_profile['city'].capitalize()} \n" \
                       f"Район города: {data_profile['area'].capitalize()} \n"

        with open(f"photos/{data_profile['url_to_photo']}.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        bot.send_message(message.chat.id, message_text,
                         reply_markup=keyboard_with_user_menu(data_profile['id'], counter))


def next_page_user_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global masters_page_questionare

    if user_state[call.message.chat.id]['masters']['page'] == user_state[call.message.chat.id]['masters'][
        'number_all_pages']:
        pass
    else:
        user_state[call.message.chat.id]['masters']['page'] += 1

    send_user_menu(call.message)


def previous_page_user_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global user_state
    if user_state[call.message.chat.id]['masters']['page'] == 1:
        pass
    else:
        user_state[call.message.chat.id]['masters']['page'] -= 1

    send_user_menu(call.message)


def send_master_url_to_telegram(call):
    url = get_master_telegram_url_by_id(call.data[len('ms_cont_'):])

    bot.send_message(call.message.chat.id, url)


def send_master_url_to_portfolio(call):
    url = get_master_portfolio_url_by_id(call.data[len('ms_port_'):])

    bot.send_message(call.message.chat.id, url)


def send_master_url_to_reviews(call):
    url = get_master_reviews_url_by_id(call.data[len('ms_reviews_'):])

    bot.send_message(call.message.chat.id, url)


def send_keyboard_with_partners(message):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception:
        pass

    try:
        bot.delete_message(message.chat.id, message.id - 1)
    except Exception:
        pass

    if 'partners' in user_state.get(message.chat.id, {}):
        pass
    else:
        user_state[message.chat.id] = {'partners': {'page': 1, 'count_pages': 1}}

    user_masters_id = get_all_partner_subscribe_profiles(message.chat.id)

    if not user_masters_id:
        bot.send_message(message.chat.id, 'Вы еще не подписались ни на один профиль')

    else:
        user_page = user_state[message.chat.id]['partners']['page']
        master_id = user_masters_id[user_page - 1]

        counter = str(user_state[message.chat.id]['partners']['page']) + '/' + str(len(user_masters_id))
        user_state[message.chat.id]['partners']['number_all_pages'] = len(user_masters_id)

        data_profile = get_masters_profiles_for_user_menu(master_id)
        message_text = f"{data_profile['username']} \n" \
                       f"{data_profile['description']} \n" \
                       f"Город: {data_profile['city']} \n" \
                       f"Район города: {data_profile['area']} \n"

        with open(f"photos/{data_profile['url_to_photo']}.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id, photo)

        bot.send_message(message.chat.id, message_text,
                         reply_markup=keyboard_with_user_partner_menu(data_profile['id'], counter))


def next_page_user_partners_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global user_state

    if user_state[call.message.chat.id]['partners']['page'] == user_state[call.message.chat.id]['partners'][
        'number_all_pages']:
        pass
    else:
        user_state[call.message.chat.id]['partners']['page'] += 1

    send_keyboard_with_partners(call.message)


def previous_page_user_partners_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)

    global user_state
    if user_state[call.message.chat.id]['partners']['page'] == 1:
        pass
    else:
        user_state[call.message.chat.id]['partners']['page'] -= 1

    send_keyboard_with_partners(call.message)


def send_master_profile_by_referall_link(message, refferal_link):
    master_id = get_master_id_by_ref_url(refferal_link)
    master = get_questionary_for_user_menu_by_id(master_id)

    with open(f"photos/{master['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    message_text = f"{master['username']} \n" \
                   f"{master['description']} \n" \
                   f"Город: {master['city'].capitalize()} \n" \
                   f"Район города: {master['area'].capitalize()} \n"

    bot.send_message(message.chat.id, message_text,
                     reply_markup=keyboard_with_master(master['id']))
