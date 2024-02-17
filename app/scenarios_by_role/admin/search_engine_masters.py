
from beauty_bot.app.scenarios_by_role.admin.service import send_menu_by_type
from beauty_bot.app.app_tools.menu_utils.admin_menu_utils import next_page_admin_menu, previous_page_admin_menu, \
    change_visibility
from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.keyboards import keyboard_with_cities_to_find_masters_profile
from beauty_bot.app.app_tools.mailing_engine import AdminMenuMasters
from beauty_bot.app.app_tools.db_queries import db


menu_with_masters = AdminMenuMasters(db)


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
    next_page_admin_menu(call, menu_with_masters)


def previous_page_admin_master_menu_by_city(call):
    previous_page_admin_menu(call, menu_with_masters)


def change_master_visibility_in_find_menu(call):
    change_visibility(call, 'masters', menu_with_masters)
