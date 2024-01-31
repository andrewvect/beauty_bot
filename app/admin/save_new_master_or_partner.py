from beauty_bot.app.admin.tools import create_message_with_successful_save_new_master
from beauty_bot.app.apps_tools.file_saver import save_image_and_get_path
from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.config import CONFIG
from beauty_bot.app.db_queries import get_area_id_by_name, add_new_master
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_towns_to_save_new_master, keyboard_with_areas_to_save_new_master, \
    admin_keyboard2, keyboard_with_master_types
from beauty_bot.app.services import generate_key

new_master_state = {}


@delete_previous_messages
def process_choose_type_master(call):
    bot.send_message(call.message.chat.id, "Выберите тип анкеты", reply_markup=keyboard_with_master_types())


@delete_previous_messages
def handle_master_type_click(call):
    if call.data[len('chose_type_'):] == 'partner':
        new_master_state['is_partner'] = True
    else:
        new_master_state['is_partner'] = False

    bot.send_message(chat_id=call.message.chat.id,
                     text="Пришлите имя мастера/партнера")

    bot.register_next_step_handler(call.message, process_new_master_username_step)


@delete_previous_messages
def process_new_master_username_step(message):
    new_master_state['username'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 1,
                          text="Пришлите фото для анкеты мастера")

    bot.register_next_step_handler(message, process_new_master_photo_step)


@delete_previous_messages
def process_new_master_photo_step(message):
    file_name = save_image_and_get_path(message, bot)

    new_master_state['file_name'] = file_name[:-3]

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 2,
                          text="Отправьте телеграмм ссылку на анкету в виде @telgram_username")

    bot.register_next_step_handler(message, process_master_telegram_id)


@delete_previous_messages
def process_master_telegram_id(message):
    new_master_state['telegram_username'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 3,
                          text="Пришлите ссылку на отзывы анкеты")

    bot.register_next_step_handler(message, process_master_reviews_url)


@delete_previous_messages
def process_master_reviews_url(message):
    new_master_state['reviews_url'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 4,
                          text="Пришлите ссылку на портфолио анкеты")

    bot.register_next_step_handler(message, process_portfolio_url)


@delete_previous_messages
def process_portfolio_url(message):
    new_master_state['portfolio_url'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 5,
                          text="Пришлите описание анкеты")

    bot.register_next_step_handler(message, process_new_master_description)


@delete_previous_messages
def process_new_master_description(message):
    new_master_state['description'] = message.text

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.id - 6,
                          text="Выберите город для анкеты")

    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns_to_save_new_master())


@delete_previous_messages
def handle_save_new_master_town(call):
    new_master_state['town'] = call.data

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id - 7,
                          text="Выберите район для мастера")

    bot.send_message(call.message.chat.id, "Доступные районы выбраного города",
                     reply_markup=keyboard_with_areas_to_save_new_master(call.data))


@delete_previous_messages
def handle_save_new_master(call):
    new_master_state['area'] = call.data[len('save_new_master_area_'):]
    area_id = get_area_id_by_name(new_master_state['area'])

    api_key = generate_key(10)
    referal_key = generate_key(10)

    add_new_master(new_master_state,
                   api_key,
                   referal_key,
                   True,
                   area_id
                   )

    bot.send_message(call.message.chat.id,
                     create_message_with_successful_save_new_master(new_master_state,
                                                                    api_key,
                                                                    referal_key,
                                                                    CONFIG))

    bot.send_message(call.message.chat.id,
                     "Меню админа",
                     reply_markup=admin_keyboard2())
