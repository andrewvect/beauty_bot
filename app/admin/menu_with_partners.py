from sqlalchemy.orm import sessionmaker

from beauty_bot.app.admin.service import send_menu_with_questionaries
from beauty_bot.app.db_queries import set_master_active_profile
from beauty_bot.app.models import engine
from beauty_bot.app.tools import AdminMenuPartners, QueriesToDb

Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)
menu_with_partners = AdminMenuPartners(queries_to_db)


def send_menu_with_partners(call):
    menu_with_partners.get_all_partners_ids()
    send_menu_with_questionaries(call, 'partners', 'new', menu_with_partners)


def next_page_partners_admin_menu(call):
    menu_with_partners.up_page()

    send_menu_with_questionaries(call, call.data[len('ad_next_page_'):], 'old', menu_with_partners)


def previous_page_partners_admin_menu(call):
    menu_with_partners.down_page()

    send_menu_with_questionaries(call, call.data[len('ad_previous_page_'):], 'old', menu_with_partners)


def change_partner_visibility(call):

    master_id = call.data[len('acv_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_questionaries(call, 'partners', 'old', menu_with_partners)

