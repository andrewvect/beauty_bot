from beauty_bot.app.app_tools.menu.AdminMenu import AdminMenuPartners
from beauty_bot.app.app_tools.menu_utils.admin_menu_utils import send_menu_with_items, next_page_admin_menu, \
    previous_page_admin_menu, change_visibility
from beauty_bot.app.app_tools.db_queries import db

menu_with_partners = AdminMenuPartners(db)


def send_menu_with_partners(call):
    send_menu_with_items(call, 'partners', menu_with_partners)


def next_page_partners_admin_menu(call):
    next_page_admin_menu(call, menu_with_partners)


def previous_page_partners_admin_menu(call):
    previous_page_admin_menu(call, menu_with_partners)


def change_partner_visibility(call):
    change_visibility(call, 'partners', menu_with_partners)

