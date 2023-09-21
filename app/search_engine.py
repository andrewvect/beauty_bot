from beauty_bot.app.db_queries import get_all_masters_id_by_name_city, get_masters_questionaries_for_admin_menu_by_city, \
    get_partners_questionaries_for_admin_menu_by_city, get_all_partners_id_by_name_city, set_master_active_profile
from beauty_bot.app.extantions import bot
from beauty_bot.app.keyboards import menu_with_questionaries_search_by_city, \
    keyboard_with_cities_to_find_masters_profile, keyboard_with_cities_to_find_partners_profile
from beauty_bot.app.services import send_menu_with_masters

page_masters_questionare = 1
page_partners_questionare = 1
all_questionaries = None
chosed_admin_city = ''


def send_cites_to_find_masters_profiles(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.delete_message(call.message.chat.id, call.message.id - 2)
    except Exception:
        pass

    bot.send_message(call.message.chat.id, 'Выберите город', reply_markup=keyboard_with_cities_to_find_masters_profile())


def send_cites_to_find_partners_profiles(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.delete_message(call.message.chat.id, call.message.id - 2)
    except Exception:
        pass

    bot.send_message(call.message.chat.id, 'Выберите город', reply_markup=keyboard_with_cities_to_find_partners_profile())


def profiles_masters_by_city(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    masters_ids = get_all_masters_id_by_name_city(call.data[3:])

    global chosed_admin_city, page_masters_questionare
    chosed_admin_city = call.data[3:]
    page_masters_questionare = 1

    if masters_ids == []:
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_masters_profiles(call)
    else:
        send_menu_with_questionaries(call, 'ct_masters', masters_ids)


def profiles_partners_by_city(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    partners_ids = get_all_partners_id_by_name_city(call.data[3:])

    global chosed_admin_city, page_partners_questionare
    chosed_admin_city = call.data[3:]
    page_partners_questionare = 1

    if partners_ids == []:
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_masters_profiles(call)
    else:
        send_menu_with_questionaries(call, 'ct_partners', partners_ids)


def send_menu_with_questionaries(call, type, masters_ids):

    data = None
    page_numbers = None

    if type == 'ct_masters':
        data = get_masters_questionaries_for_admin_menu_by_city(page_masters_questionare, masters_ids)
        page_numbers = f"{page_masters_questionare}/{data['page_counter']}"
    if type == 'ct_partners':
        data = get_partners_questionaries_for_admin_menu_by_city(page_partners_questionare, masters_ids)
        page_numbers = f"{page_partners_questionare}/{data['page_counter']}"

    message = f"{data['questionary']['description']} \n" \
              f"Город: {data['questionary']['city_name']} \n" \
              f"Район города: {data['questionary']['area_name']} \n"

    global all_questionaries
    all_questionaries = data['page_counter']

    with open(f"photos/{data['questionary']['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo)

    bot.send_message(call.message.chat.id, message)

    bot.send_message(call.message.chat.id, "Меню:",
                     reply_markup=menu_with_questionaries_search_by_city(data['questionary']['is_active'],
                                                                         page_numbers,
                                                                         type,
                                                                         data['questionary']['master_id']))


def next_page_admin_master_menu_by_city(call):
    for i in range(3):
        try:
            bot.delete_message(call.message.chat.id, call.message.id - i)
        except Exception:
            pass

    global page_masters_questionare

    if page_masters_questionare == all_questionaries:
        pass
    else:
        page_masters_questionare += 1

    master_ids = get_all_masters_id_by_name_city(chosed_admin_city)

    send_menu_with_questionaries(call, call.data[len('ad_f_next_'):], master_ids)


def previous_page_admin_master_menu_by_city(call):
    for i in range(3):
        try:
            bot.delete_message(call.message.chat.id, call.message.id - i)
        except Exception:
            pass

    global page_masters_questionare
    if page_masters_questionare == 1:
        pass
    else:
        page_masters_questionare -= 1

    master_ids = get_all_masters_id_by_name_city(chosed_admin_city)

    send_menu_with_questionaries(call, call.data[len('ad_f_previous_'):], master_ids)


def next_page_admin_partner_menu_by_city(call):
    for i in range(3):
        try:
            bot.delete_message(call.message.chat.id, call.message.id - i)
        except Exception:
            pass

    global page_partners_questionare

    if page_partners_questionare == all_questionaries:
        pass
    else:
        page_partners_questionare += 1

    master_ids = get_all_partners_id_by_name_city(chosed_admin_city)

    send_menu_with_questionaries(call, call.data[len('ad_f_next_'):], master_ids)


def previous_page_admin_partner_menu_by_city(call):
    for i in range(3):
        try:
            bot.delete_message(call.message.chat.id, call.message.id - i)
        except Exception:
            pass

    global page_partners_questionare
    if page_partners_questionare == 1:
        pass
    else:
        page_partners_questionare -= 1

    master_ids = get_all_partners_id_by_name_city(chosed_admin_city)
    send_menu_with_questionaries(call, call.data[len('ad_f_previous_'):], master_ids)


def change_partner_visibility_in_find_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)
    bot.delete_message(call.message.chat.id, call.message.id - 2)

    master_id = call.data[len('acvF_') + 1:]
    set_master_active_profile(master_id)

    master_ids = get_all_masters_id_by_name_city(chosed_admin_city)

    send_menu_with_questionaries(call, 'ct_masters', master_ids)


def change_master_visibility_in_find_menu(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, call.message.id - 1)
    bot.delete_message(call.message.chat.id, call.message.id - 2)

    master_id = call.data[len('acvF_') + 1:]
    set_master_active_profile(master_id)

    master_ids = get_all_partners_id_by_name_city(chosed_admin_city)

    send_menu_with_questionaries(call, 'ct_masters', master_ids)

