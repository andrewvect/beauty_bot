
from beauty_bot.app.keyboards import keyboard_with_user_menu
from beauty_bot.app.services import queries_to_db
from beauty_bot.app.tools import MenuWithQuestionnairesEngine
from beauty_bot.app.user.user_masters_menu import user_state
from beauty_bot.extantions import bot


def get_last_message_id(chat_id):
    message = bot.send_message('привет', chat_id)


def send_menu_with_questionarties_by_type(message, description, url_to_photo, user_id, master_tg_username):
    if user_id in user_state:
        menu = user_state[user_id]['masters']
    else:
        menu = MenuWithQuestionnairesEngine(queries_to_db, user_id)
        user_state[user_id] = {'masters': menu}

    master_id = queries_to_db.get_master_id_by_telegram_user_name(master_tg_username)
    menu.move_number_to_first(master_id)
    menu.get_data_for_questionary()

    if url_to_photo is None:
        url_to_photo = menu.master_data['url_to_photo']

    message_text = f"Вам сообщение от {menu.master_data['username']} \n" \
                   f"{description} \n"

    with open(f"beauty_bot/app/photos/{url_to_photo}.jpg", 'rb') as photo:
        bot.send_photo(user_id,
                       caption=message_text,
                       photo=photo,
                       reply_markup=keyboard_with_user_menu(menu.master_data['id'],
                                                            menu.count_numbers(),
                                                            menu.master_data['reviews_url'],
                                                            menu.master_data['master_portfolio_url'],
                                                            menu.master_data['telegram_user_name'],
                                                            menu.master_data['location_id']))
