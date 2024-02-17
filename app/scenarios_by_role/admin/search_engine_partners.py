from beauty_bot.app.scenarios_by_role.admin.service import send_menu_by_type
from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.app.app_tools.menu_utils.admin_menu_utils import next_page_admin_menu, previous_page_admin_menu, \
    change_visibility
from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.AdminKeyboards import admin_keyboards
from beauty_bot.app.app_tools.mailing_engine import AdminMenuPartners

menu_with_partners = AdminMenuPartners(db)


@delete_previous_messages
def send_cites_to_find_partners_profiles(call) -> None:
    bot.send_message(call.message.chat.id, 'Выберите город',
                     reply_markup=admin_keyboards.keyboard_with_cities_to_find_partners_profile())


@delete_previous_messages
def profiles_partners_by_city(call) -> None:
    menu_with_partners.selected_city_for_partners = call.data[3:]

    try:
        menu_with_partners.get_partners_ids_by_city_name()
    except Exception:
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_partners_profiles(call)
    else:
        send_menu_with_partners_questionaries(call, 'new')


def send_menu_with_partners_questionaries(call, state) -> None:
    menu_with_partners.get_data_for_questionary()

    send_menu_by_type(call, state, 'P', menu_with_partners)


def next_page_admin_partner_menu_by_city(call) -> None:
    next_page_admin_menu(call, menu_with_partners)


def previous_page_admin_partner_menu_by_city(call) -> None:
    previous_page_admin_menu(call, menu_with_partners)


def change_partner_visibility_in_find_menu(call) -> None:
    change_visibility(call, 'partners', menu_with_partners)
