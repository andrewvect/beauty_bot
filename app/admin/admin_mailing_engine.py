from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.keyboards import keyboard_with_mailing_type_for_admin, keyboard_with_cities_for_admin_mailing, \
    keyboard_with_districts_for_admin_mailing, keyboard_to_srart_mailing_for_amdin, admin_keyboard2
from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.app.app_tools.file_saver import save_image_and_get_path

mailing = MailingEngine(db)


@delete_previous_messages
def send_keyboard_with_mailing_type_for_admin(call) -> None:
    bot.send_message(call.message.chat.id, "Выберите тип рассылки:",
                     reply_markup=keyboard_with_mailing_type_for_admin())


@delete_previous_messages
def process_answer_for_new_admin_mailing_with_photo(call) -> None:
    bot.register_next_step_handler(call.message, process_save_photo_for_new_mailing)

    bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


@delete_previous_messages
def process_answer_for_new_mailing_without_photo_as_admin(call) -> None:
    bot.send_message(call.message.chat.id, "Пришлите описание для рассылки")

    bot.register_next_step_handler(call.message, process_save_description_for_new_mailing_as_admin)


@delete_previous_messages
def process_save_photo_for_new_mailing(message) -> None:

    mailing.url_to_photo = save_image_and_get_path(message, bot)

    bot.send_message(message.chat.id, "Пришлите описание для рассылки")

    bot.register_next_step_handler(message, process_save_description_for_new_mailing_as_admin)


@delete_previous_messages
def process_save_description_for_new_mailing_as_admin(message) -> None:

    mailing.description = message.text

    bot.send_message(message.chat.id, 'Выберите город для рассылки',
                     reply_markup=keyboard_with_cities_for_admin_mailing())


@delete_previous_messages
def process_save_city_for_new_mailing_as_admin(call) -> None:

    mailing.city = call.data[len('ad_ml_c'):]

    bot.send_message(call.message.chat.id, "Выберите район для рассылки",
                     reply_markup=keyboard_with_districts_for_admin_mailing(call.data))


@delete_previous_messages
def process_save_area_for_new_mailing_as_admin(call) -> None:

    mailing.district = call.data[len('ad_ml_dist_'):]

    bot.send_message(call.message.chat.id, 'Управление рассылкой', reply_markup=keyboard_to_srart_mailing_for_amdin())


@delete_previous_messages
def start_mailing_as_admin(call) -> None:
    mailing.fill_users()
    mailing.start_mailing(call.message.chat.id, bot)

    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
