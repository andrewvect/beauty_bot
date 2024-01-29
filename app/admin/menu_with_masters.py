from sqlalchemy.orm import sessionmaker

from beauty_bot.app.admin.service import send_menu_with_questionaries
from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.db_queries import set_master_active_profile
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import admin_keyboard2
from beauty_bot.app.models import engine
from beauty_bot.app.tools import QueriesToDb, AdminMenuMasters

Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)
menu_with_masters = AdminMenuMasters(queries_to_db)


@delete_previous_messages
def admin_logout(call) -> None:
    pass


@delete_previous_messages
def return_to_admin_menu(call):
    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


def send_menu_with_masters(call):
    menu_with_masters.get_all_masters()
    send_menu_with_questionaries(call, 'masters', 'new', menu_with_masters)


def next_page_masters_admin_menu(call):
    menu_with_masters.up_page()

    send_menu_with_questionaries(call, call.data[len('ad_next_page_'):], 'old', menu_with_masters)


def previous_page_masters_admin_menu(call):
    menu_with_masters.down_page()

    send_menu_with_questionaries(call, call.data[len('ad_previous_page_'):], 'old', menu_with_masters)


@delete_previous_messages
def back_to_admin_menu_from_questionaries(call):
    bot.send_message(call.message.chat.id, "Меню админа:", reply_markup=admin_keyboard2())


@delete_previous_messages
def back_to_admin_menu_create_questionary(call):

    bot.send_message(call.message.chat.id, "Меню админа:", reply_markup=admin_keyboard2())


def change_master_visibility(call):
    master_id = call.data[len('acv_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_questionaries(call, 'masters', 'old', menu_with_masters)
