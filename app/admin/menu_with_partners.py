from sqlalchemy.orm import sessionmaker
from beauty_bot.app.apps_tools.menu_utils.admin_menu_utils import send_menu_with_items, next_page_admin_menu, \
    previous_page_admin_menu, change_visibility
from beauty_bot.app.models import engine
from beauty_bot.app.tools import AdminMenuPartners, QueriesToDb

Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)
menu_with_partners = AdminMenuPartners(queries_to_db)


def send_menu_with_masters(call):
    send_menu_with_items(call, 'partners', menu_with_partners)


def next_page_masters_admin_menu(call):
    next_page_admin_menu(call, menu_with_partners)


def previous_page_masters_admin_menu(call):
    previous_page_admin_menu(call, menu_with_partners)


def change_master_visibility(call):
    change_visibility(call, 'partners', menu_with_partners)

