
# save new master questionnaire
import traceback

from beauty_bot.app.config import bot_name_tg
from beauty_bot.app.db_queries import get_area_id_by_name, add_new_master
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_towns_to_save_new_master, keyboard_with_areas_to_save_new_master, \
    admin_keyboard2, keyboard_with_master_types
from beauty_bot.app.logger import log_error
from beauty_bot.app.services import generate_key

new_master_state = {}


def process_choose_type_master(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, "Выберите тип анкеты", reply_markup=keyboard_with_master_types())


def handle_master_type_click(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)

        count = len('chose_type_')
        if call.data[count:] == 'partner':
            new_master_state['is_partner'] = True
        else:
            new_master_state['is_partner'] = False

        bot.send_message(chat_id=call.message.chat.id,
                         text="Пришлите имя мастера/партнера")

        bot.register_next_step_handler(call.message, process_new_master_username_step)
    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_new_master_username_step(message):
    try:
        bot.delete_message(message.chat.id, message.id)

        new_master_state['username'] = message.text

        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 1,
                              text="Пришлите фото для анкеты мастера")

        bot.register_next_step_handler(message, process_new_master_photo_step)
    except Exception as e:
        print(traceback.TracebackException)
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_new_master_photo_step(message):
    try:

        photo = message.photo[-1]
        file_id = photo.file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        file_name = generate_key(7)

        with open(f'beauty_bot/app/photos/{file_name}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        new_master_state['file_name'] = file_name
        bot.delete_message(message.chat.id, message.id)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 2,
                              text="Отправьте телеграмм ссылку на анкету в виде @telgram_username")

        bot.register_next_step_handler(message, process_master_telegram_id)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_master_telegram_id(message):
    try:

        new_master_state['telegram_username'] = message.text

        bot.delete_message(message.chat.id, message.id)

        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 3,
                              text="Пришлите ссылку на отзывы анкеты")

        bot.register_next_step_handler(message, process_master_reviews_url)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_master_reviews_url(message):
    try:
        bot.delete_message(message.chat.id, message.id)

        new_master_state['reviews_url'] = message.text

        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 4,
                              text="Пришлите ссылку на портфолио анкеты")

        bot.register_next_step_handler(message, process_portfolio_url)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_portfolio_url(message):
    try:
        bot.delete_message(message.chat.id, message.id)

        new_master_state['portfolio_url'] = message.text

        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 5,
                              text="Пришлите описание анкеты")

        bot.register_next_step_handler(message, process_new_master_description)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды")


def process_new_master_description(message):
    bot.delete_message(message.chat.id, message.id)

    new_master_state['description'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 6,
                          text="Выберите город для анкеты")

    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns_to_save_new_master())


def handle_save_new_master_town(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    new_master_state['town'] = call.data

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id - 7,
                          text="Выберите район для мастера")

    bot.send_message(call.message.chat.id, "Доступные районы выбраного города",
                     reply_markup=keyboard_with_areas_to_save_new_master(call.data))


def handle_save_new_master(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    new_master_state['area'] = call.data[len('save_new_master_area_'):]
    area_id = get_area_id_by_name(new_master_state['area'])

    api_key = generate_key(10)
    referal_key = generate_key(10)

    add_new_master(new_master_state['telegram_username'],
                   api_key,
                   referal_key,
                   new_master_state['description'],
                   new_master_state['username'],
                   new_master_state['file_name'],
                   new_master_state['is_partner'],
                   True,
                   area_id,
                   new_master_state['reviews_url'],
                   new_master_state['portfolio_url']
                   )

    value = 'мастера'
    if new_master_state['is_partner']:
        value = 'партнера'

    bot.send_message(call.message.chat.id, f"Анкета {value} {new_master_state['username']} создана!\n"
                                           f"Api key: {api_key} \n"
                                           f"Referal link: https://t.me/{bot_name_tg[1:]}?start={referal_key}")
    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())

