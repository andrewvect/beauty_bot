import traceback

from sqlalchemy.orm import sessionmaker
from telebot import types

from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.keyboards import keyboard_with_user_partner_menu
from beauty_bot.app.models import engine
from beauty_bot.app.app_tools.mailing_engine import MenuWithPartnersQuestionnaires, QueriesToDb
from beauty_bot.app.scenarios_by_role.user.user_masters_menu import send_menu_with_questionarties_masters

user_state = {}
Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)


def process_partners_menu(call):
    area_id = call.data[len('partners_mn_'):]

    if call.message.chat.id not in user_state:
        user_state[call.message.chat.id] = {}

    user_state[call.message.chat.id]['partners'] = MenuWithPartnersQuestionnaires(queries_to_db, call.message.chat.id,
                                                                                  area_id)
    send_keyboard_with_partners(call, 'new')


def next_page_user_partners_menu(call):
    menu = user_state[call.message.chat.id]['partners']
    menu.up_page()

    send_keyboard_with_partners(call, 'old')


def previous_page_user_partners_menu(call):
    menu = user_state[call.message.chat.id]['partners']
    menu.down_page()

    send_keyboard_with_partners(call, 'old')


def send_keyboard_with_partners(call, state):
    menu = user_state[call.message.chat.id]['partners']

    if not menu.content_ids:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.delete_message(call.message.chat.id, call.message.id - 1)
        bot.send_message(call.message.chat.id, 'У мастера еще нет партнеров')
        send_menu_with_questionarties_masters(call.message)

    else:
        menu.get_data_for_questionary()
        message_text = f"{menu.master_data['username']} \n" \
                       f"{menu.master_data['description']} \n"

        if state == 'new':
            try:
                with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
                    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.id,
                                           reply_markup=keyboard_with_user_partner_menu(menu.master_data['id'],
                                                                                        menu.count_numbers(),
                                                                                        menu.master_data['reviews_url'],
                                                                                        menu.master_data[
                                                                                            'master_portfolio_url'],
                                                                                        menu.master_data[
                                                                                            'telegram_user_name']))
            except Exception:
                print(traceback.print_exc())
                pass

            try:
                bot.edit_message_caption(chat_id=call.message.chat.id, caption=message_text, message_id=call.message.id,
                                         reply_markup=keyboard_with_user_partner_menu(menu.master_data['id'],
                                                                                      menu.count_numbers(),
                                                                                      menu.master_data['reviews_url'],
                                                                                      menu.master_data[
                                                                                          'master_portfolio_url'],
                                                                                      menu.master_data[
                                                                                          'telegram_user_name']))
            except Exception:
                pass

        if state == 'old':
            try:
                with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
                    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.id,
                                           reply_markup=keyboard_with_user_partner_menu(menu.master_data['id'],
                                                                                        menu.count_numbers(),
                                                                                        menu.master_data['reviews_url'],
                                                                                        menu.master_data[
                                                                                            'master_portfolio_url'],
                                                                                        menu.master_data[
                                                                                            'telegram_user_name']))
            except Exception:
                print(traceback.print_exc())
                pass

            try:
                bot.edit_message_caption(chat_id=call.message.chat.id, caption=message_text, message_id=call.message.id,
                                         reply_markup=keyboard_with_user_partner_menu(menu.master_data['id'],
                                                                                      menu.count_numbers(),
                                                                                      menu.master_data['reviews_url'],
                                                                                      menu.master_data[
                                                                                          'master_portfolio_url'],
                                                                                      menu.master_data[
                                                                                          'telegram_user_name']))
            except Exception:
                pass
