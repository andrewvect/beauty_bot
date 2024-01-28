import traceback

from sqlalchemy.orm import sessionmaker
from telebot import types

from beauty_bot.app.db_queries import set_master_active_profile
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_cities_to_find_partners_profile, \
    menu_with_questionaries_search_by_city
from beauty_bot.app.models import engine
from beauty_bot.app.tools import QueriesToDb, AdminMenuPartners

Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)
menu_with_partners = AdminMenuPartners(queries_to_db)


def send_cites_to_find_partners_profiles(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.delete_message(call.message.chat.id, call.message.id - 2)
    except Exception:
        pass

    bot.send_message(call.message.chat.id, 'Выберите город',
                     reply_markup=keyboard_with_cities_to_find_partners_profile())


def profiles_partners_by_city(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    menu_with_partners.selected_city_for_partners = call.data[3:]

    try:
        menu_with_partners.get_partners_ids_by_city_name()
        send_menu_with_partners_questionaries(call, 'new')
    except Exception:
        print(traceback.print_exc())
        bot.send_message(call.message.chat.id, 'В выбранном городе еще нет анкет.')
        send_cites_to_find_partners_profiles(call)


def send_menu_with_partners_questionaries(call, state):
    menu_with_partners.get_data_for_questionary()
    data = menu_with_partners.master_data

    if state == 'new':
        with open(f"beauty_bot/app/photos/{data['url_to_photo']}.jpg", 'rb') as photo:
            bot.send_photo(chat_id=call.message.chat.id, photo=photo,
                           reply_markup=menu_with_questionaries_search_by_city(data['is_active'],
                                                                               menu_with_partners.count_numbers(),
                                                                               'P',
                                                                               data['id']),
                           caption=menu_with_partners.get_description())

    if state == 'old':
        try:
            with open(f"beauty_bot/app/photos/{data['url_to_photo']}.jpg", 'rb') as photo:
                bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                                       chat_id=call.message.chat.id,
                                       message_id=call.message.id,
                                       reply_markup=menu_with_questionaries_search_by_city(data['is_active'],
                                                                                           menu_with_partners.count_numbers(),
                                                                                           'P',
                                                                                           data['id']))

                bot.edit_message_caption(caption=menu_with_partners.get_description(),
                                         chat_id=call.message.chat.id,
                                         message_id=call.message.id,
                                         reply_markup=menu_with_questionaries_search_by_city(data['is_active'],
                                                                                             menu_with_partners.count_numbers(),
                                                                                             'P',
                                                                                             data['id']))
        except Exception:
            print(traceback.print_exc())


def next_page_admin_partner_menu_by_city(call):
    menu_with_partners.up_page()

    send_menu_with_partners_questionaries(call, 'old')


def previous_page_admin_partner_menu_by_city(call):
    menu_with_partners.down_page()

    send_menu_with_partners_questionaries(call, 'old')


def change_partner_visibility_in_find_menu(call):
    master_id = call.data[len('acvF_') + 1:]
    set_master_active_profile(master_id)

    send_menu_with_partners_questionaries(call, 'old')