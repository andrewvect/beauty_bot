# menu_utils.py
from beauty_bot.app.scenarios_by_role.admin import send_menu_with_questionaries
from beauty_bot.app.app_tools.db_queries import db


def send_menu_with_items(call, menu_type, menu_instance):
    menu_instance.get_all_items()
    send_menu_with_questionaries(call, menu_type, 'new', menu_instance)


def next_page_admin_menu(call, menu_instance):
    menu_instance.up_page()
    send_menu_with_questionaries(call, call.data[len('ad_next_page_'):], 'old', menu_instance)


def previous_page_admin_menu(call, menu_instance):
    menu_instance.down_page()
    send_menu_with_questionaries(call, call.data[len('ad_previous_page_'):], 'old', menu_instance)


def change_visibility(call, menu_type, menu_instance):
    db.set_master_active_profile(master_id=call.data[len('acv_') + 1:])
    send_menu_with_questionaries(call, menu_type, 'old', menu_instance)
