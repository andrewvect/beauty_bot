from sqlalchemy.orm import sessionmaker

from beauty_bot.app.admin.tools import send_menu_with_photo, edit_message
from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.db_queries import set_master_active_profile
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_cities_to_find_masters_profile, \
    menu_with_questionaries_search_by_city
from beauty_bot.app.models import engine
from beauty_bot.app.tools import QueriesToDb, AdminMenuMasters

Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)
menu_with_masters = AdminMenuMasters(queries_to_db)


@delete_previous_messages
def send_cites_to_find_masters_profiles(call):
    bot.send_message(call.message.chat.id, 'Выберите город',
                     reply_markup=keyboard_with_cities_to_find_masters_profile())


@delete_previous_messages
def profiles_masters_by_city(call):
    menu_with_masters.selected_city_for_masters = call.data[3:]

    try:
        menu_with_masters.get_masters_ids_by_city_name()
        send_menu_with_master_questionaries(call, 'new')
    except Exception:
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_masters_profiles(call)


def send_menu_with_master_questionaries(call, state):
    menu_with_masters.get_data_for_questionary()

    if state == 'new':
        send_menu_with_photo(call, 'M', menu_with_masters,
                             menu_with_questionaries_search_by_city(menu_with_masters, 'M'), menu_with_masters.get_description())

    if state == 'old':
        edit_message(call, menu_with_masters, menu_with_questionaries_search_by_city(menu_with_masters, 'M'),
                     menu_with_masters.get_description(), 'M')


def next_page_admin_master_menu_by_city(call):
    menu_with_masters.up_page()

    send_menu_with_master_questionaries(call, 'old')


def previous_page_admin_master_menu_by_city(call):
    menu_with_masters.down_page()

    send_menu_with_master_questionaries(call, 'old')


def change_master_visibility_in_find_menu(call):
    master_id = call.data[len('acvF_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_master_questionaries(call, 'old')
