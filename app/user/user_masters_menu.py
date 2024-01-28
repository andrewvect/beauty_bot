import traceback

from telebot import types

from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_user_menu
from beauty_bot.app.services import queries_to_db
from beauty_bot.app.tools import MenuWithQuestionnairesEngine

user_state = {}


def next_page_user_menu(call):
    print(user_state)
    menu = user_state[call.message.chat.id]['masters']
    menu.up_page()

    send_menu_with_questionarties_by_type(call.message, 'masters', 'old')


def previous_page_user_menu(call):
    menu = user_state[call.message.chat.id]['masters']
    menu.down_page()

    send_menu_with_questionarties_by_type(call.message, 'masters', 'old')


def subscribe_on_master(message, referral_link):
    queries_to_db.subscribe_user_on_master_with_referral_link(referral_link, message.chat.id)

    menu = MenuWithQuestionnairesEngine(queries_to_db, message.chat.id)
    menu.set_referral_link(referral_link)
    if message.chat.id not in user_state:
        user_state[message.chat.id] = {}
    user_state[message.chat.id]['masters'] = menu

    send_menu_with_questionarties_masters(message)


def send_menu_with_questionarties_by_type(message, type, state):
    print(user_state)
    if message.chat.id in user_state:
        menu = user_state[message.chat.id][type]
    else:

        menu = MenuWithQuestionnairesEngine(queries_to_db, message.chat.id)
        user_state[message.chat.id] = {type: menu}

    menu.get_data_for_questionary()

    message_text = f"{menu.master_data['username']} \n" \
                   f"{menu.master_data['description']} \n"

    if state == 'new':
        with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id,
                           caption=message_text,
                           photo=photo,
                           reply_markup=keyboard_with_user_menu(menu.master_data['id'],
                                                                menu.count_numbers(),
                                                                menu.master_data['reviews_url'],
                                                                menu.master_data['master_portfolio_url'],
                                                                menu.master_data['telegram_user_name'],
                                                                menu.master_data['location_id']))

    if state == 'old':
        try:
            with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
                bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                                       chat_id=message.chat.id,
                                       message_id=message.id,
                                       reply_markup=keyboard_with_user_menu(menu.master_data['id'],
                                                                            menu.count_numbers(),
                                                                            menu.master_data['reviews_url'],
                                                                            menu.master_data['master_portfolio_url'],
                                                                            menu.master_data['telegram_user_name'],
                                                                            menu.master_data['location_id']))

                bot.edit_message_caption(caption=message_text, chat_id=message.chat.id, message_id=message.id,
                                         reply_markup=keyboard_with_user_menu(menu.master_data['id'],
                                                                              menu.count_numbers(),
                                                                              menu.master_data['reviews_url'],
                                                                              menu.master_data['master_portfolio_url'],
                                                                              menu.master_data['telegram_user_name'],
                                                                              menu.master_data['location_id']))
        except Exception:
            print(traceback.print_exc())


def send_menu_with_questionarties_masters(message):
    send_menu_with_questionarties_by_type(message, 'masters', 'new')


def send_menu_with_questionarties_masters2(message):
    send_menu_with_questionarties_by_type(message, 'masters', 'old')
