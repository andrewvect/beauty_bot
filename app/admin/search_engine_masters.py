from sqlalchemy.orm import sessionmaker
from beauty_bot.app.admin.service import send_menu_by_type
from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.db_queries import set_master_active_profile
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_cities_to_find_masters_profile
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
    except Exception:
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_masters_profiles(call)
    else:
        send_menu_with_master_questionaries(call, 'new')


def send_menu_with_master_questionaries(call, state):
    menu_with_masters.get_data_for_questionary()

    send_menu_by_type(call, state, 'M', menu_with_masters)


def next_page_admin_master_menu_by_city(call):
    menu_with_masters.up_page()

    send_menu_with_master_questionaries(call, 'old')


def previous_page_admin_master_menu_by_city(call):
    menu_with_masters.down_page()

    send_menu_with_master_questionaries(call, 'old')


def change_master_visibility_in_find_menu(call):
    set_master_active_profile(master_id=call.data[len('acvF_') + 1:])

    send_menu_with_master_questionaries(call, 'old')
