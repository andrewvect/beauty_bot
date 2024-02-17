from beauty_bot.app.app_tools.file_saver import save_image_and_get_path
from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.app.scenarios_by_role.master.send_menu_with_mailing import send_menu_with_questionarties_by_type
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.keyboards import keyboard_master_menu, keyboard_to_srart_mailing, keyboard_with_mailing_type

new_masters_mailing_state = dict()


@delete_previous_messages
def send_keyboard_with_master_menu(message) -> None:
    bot.send_message(message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


@delete_previous_messages
def send_keyboard_with_mailing_type(call) -> None:
    new_masters_mailing_state[call.message.chat.id] = {}

    bot.send_message(call.message.chat.id, "Выберите тип рассылки:", reply_markup=keyboard_with_mailing_type())


@delete_previous_messages
def process_answer_for_new_mailing_with_photo(call) -> None:
    bot.send_message(call.message.chat.id, "Пришлите фото для рассылки")

    bot.register_next_step_handler(call.message, process_save_photo_for_new_mailing)


@delete_previous_messages
def process_answer_for_new_mailing_without_photo(call) -> None:
    bot.send_message(call.message.chat.id, "Пришлите описание для рассылки")
    bot.register_next_step_handler(call.message, process_save_description_for_new_mailing)


@delete_previous_messages
def process_save_photo_for_new_mailing(message) -> None:
    file_name = save_image_and_get_path(message, bot)

    new_masters_mailing_state[message.chat.id]['photo'] = file_name[:-4]

    bot.send_message(message.chat.id, "Пришлите описание для рассылки")

    bot.register_next_step_handler(message, process_save_description_for_new_mailing)


@delete_previous_messages
def process_save_description_for_new_mailing(message) -> None:
    new_masters_mailing_state[message.chat.id]['description'] = message.text

    message_text = f"{new_masters_mailing_state[message.chat.id]['description']} \n" \
                   f"Контакт: @{message.from_user.username}"

    if len(new_masters_mailing_state[message.chat.id]) == 1:
        photo_master_from_db = db.get_master_photo_name_by_telegram_username('@' + message.chat.username)
        new_masters_mailing_state[message.chat.id]['photo'] = photo_master_from_db

    with open(f"beauty_bot/app/photos/{new_masters_mailing_state[message.chat.id]['photo'] + '.jpg'}",
              'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=message_text)

    bot.send_message(message.chat.id, 'Управление рассылкой', reply_markup=keyboard_to_srart_mailing())


@delete_previous_messages
def start_mailing(call) -> None:
    subscribers_telegram_ids = db.get_all_master_subscribers_by_master_telegram_username(call.message.chat.username)

    if not subscribers_telegram_ids:
        bot.send_message(call.message.chat.id, "У вас еще нет подписчиков")

    if not db.check_master_visability(call.message.chat.username):
        return bot.send_message(call.message.chat.id, 'Ваша анкета сейчас не активна, расслыка не возможна')

    else:

        bot.send_message(call.message.chat.id, "Рассылка запущена")

        for user_id in subscribers_telegram_ids:
            send_menu_with_questionarties_by_type(
                new_masters_mailing_state[call.message.chat.id],
                user_id,
                call.message.chat.username)

    bot.send_message(call.message.chat.id, "Личный кабинет мастера 🧑:", reply_markup=keyboard_master_menu())


# authorisation as master
def check_master_key(user_name, key):
    user_key = db.get_key_by_telegram_username('@' + user_name)
    if user_key.lower() == key:
        return True
    return False
