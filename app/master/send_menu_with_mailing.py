from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.app.app_tools.keyboards.keyboards import keyboard_with_user_menu
from beauty_bot.app.app_tools.tools import MenuWithQuestionnairesEngine
from beauty_bot.app.user.user_masters_menu import user_state
from beauty_bot.extantions import bot


def send_menu_with_questionarties_by_type(master, user_id, master_tg_username) -> None:

    if user_id in user_state:
        menu = user_state[user_id]['masters']
    else:
        menu = MenuWithQuestionnairesEngine(db, user_id)
        user_state[user_id] = {'masters': menu}

    master_id = db.get_master_id_by_telegram_user_name(master_tg_username)
    menu.move_number_to_first(master_id)
    menu.get_data_for_questionary()

    if master['url_to_photo']:
        master['url_to_photo'] = menu.master_data['url_to_photo']

    message_text = f"Вам сообщение от {menu.master_data['username']} \n" \
                   f"{master['description']} \n"

    with open(f"beauty_bot/app/photos/{master['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(user_id,
                       caption=message_text,
                       photo=photo,
                       reply_markup=keyboard_with_user_menu(menu))
