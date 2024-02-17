from beauty_bot.app.app_tools.menu.AdminMenu import AdminMenuMasters
from beauty_bot.app.app_tools.menu_utils.admin_menu_utils import send_menu_with_items, next_page_admin_menu, \
    previous_page_admin_menu, change_visibility
from beauty_bot.app.app_tools.db_queries import db

menu_with_masters = AdminMenuMasters(db)


def send_menu_with_masters(call):
    send_menu_with_items(call, 'masters', menu_with_masters)


def next_page_masters_admin_menu(call):
    next_page_admin_menu(call, menu_with_masters)


def previous_page_masters_admin_menu(call):
    previous_page_admin_menu(call, menu_with_masters)


def change_master_visibility(call):
    change_visibility(call, 'masters', menu_with_masters)