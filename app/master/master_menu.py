"""
master menu with mailing
"""
import traceback

from sqlalchemy.orm import sessionmaker

from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.db_queries import get_master_photo_name_by_telegram_username, \
    get_all_master_subscribers_by_master_telegram_username, get_key_by_telegram_username
from beauty_bot.app.master.send_menu_with_mailing import send_menu_with_questionarties_by_type
from beauty_bot.app.models import engine
from beauty_bot.app.tools import QueriesToDb
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_master_menu, keyboard_to_srart_mailing, keyboard_with_mailing_type
from beauty_bot.app.logger import log_error
from beauty_bot.app.services import generate_key

new_masters_mailing_state = dict()
Session = sessionmaker(bind=engine)
queries_to_db = QueriesToDb(Session)


@delete_previous_messages
def send_keyboard_with_master_menu(message):
    bot.send_message(message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


@delete_previous_messages
def send_keyboard_with_mailing_type(call):
    new_masters_mailing_state[call.message.chat.id] = {}

    bot.send_message(call.message.chat.id, "Выберите тип рассылки:", reply_markup=keyboard_with_mailing_type())


@delete_previous_messages
def process_answer_for_new_mailing_with_photo(call):
    bot.send_message(call.message.chat.id, "Пришлите фото для рассылки")

    bot.register_next_step_handler(call.message, process_save_photo_for_new_mailing)


@delete_previous_messages
def process_answer_for_new_mailing_without_photo(call):
    bot.send_message(call.message.chat.id, "Пришлите описание для рассылки")
    bot.register_next_step_handler(call.message, process_save_description_for_new_mailing)


@delete_previous_messages
def process_save_photo_for_new_mailing(message):
    photo = message.photo[-1]
    file_id = photo.file_id

    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    downloaded_file = bot.download_file(file_path)

    file_name = generate_key(7)

    with open(f'beauty_bot/app/photos/{file_name}.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

    new_masters_mailing_state[message.chat.id]['photo'] = file_name

    bot.send_message(message.chat.id, "Пришлите описание для рассылки")

    bot.register_next_step_handler(message, process_save_description_for_new_mailing)


@delete_previous_messages
def process_save_description_for_new_mailing(message):

    new_masters_mailing_state[message.chat.id]['description'] = message.text

    message_text = f"{new_masters_mailing_state[message.chat.id]['description']} \n" \
                   f"Контакт: @{message.from_user.username}"

    if len(new_masters_mailing_state[message.chat.id]) == 1:
        photo_master_name = get_master_photo_name_by_telegram_username('@' + message.chat.username)
        new_masters_mailing_state[message.chat.id]['photo'] = photo_master_name

        with open(f"beauty_bot/app/photos/{photo_master_name + '.jpg'}", 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=message_text)

    else:
        with open(f"beauty_bot/app/photos/{new_masters_mailing_state[message.chat.id]['photo'] + '.jpg'}",
                  'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=message_text)

    bot.send_message(message.chat.id, 'Управление рассылкой', reply_markup=keyboard_to_srart_mailing())


@delete_previous_messages
def start_mailing(call):

    subscribers_telegram_ids = get_all_master_subscribers_by_master_telegram_username(call.message.chat.username)

    if not subscribers_telegram_ids:
        bot.send_message(call.message.chat.id, "У вас еще нет подписчиков")

    if not queries_to_db.check_master_visability(call.message.chat.username):
        return bot.send_message(call.message.chat.id, 'Ваша анкета сейчас не активна, расслыка не возможна')
    else:
        try:
            bot.send_message(call.message.chat.id, "Рассылка запущена")

            for user_id in subscribers_telegram_ids:
                send_menu_with_questionarties_by_type(call.message,
                                                      new_masters_mailing_state[call.message.chat.id]['description'],
                                                      new_masters_mailing_state[call.message.chat.id]['photo'],
                                                      user_id,
                                                      call.message.chat.username)

        except Exception:
            print(traceback.print_exc())

    bot.send_message(call.message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


# authorisation as master
def check_master_key(user_name, key):
    user_key = get_key_by_telegram_username('@' + user_name)
    if user_key.lower() == key:
        return True
    return False
