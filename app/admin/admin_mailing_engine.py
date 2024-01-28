from sqlalchemy.orm import sessionmaker

from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import keyboard_with_mailing_type_for_admin, keyboard_with_cities_for_admin_mailing, \
    keyboard_with_districts_for_admin_mailing, keyboard_to_srart_mailing_for_amdin, admin_keyboard2
from beauty_bot.app.logger import log_error
from beauty_bot.app.models import engine
from beauty_bot.app.services import generate_key
from beauty_bot.app.tools import QueriesToDb, MailingEngine

Session = sessionmaker(bind=engine)

queries_to_db = QueriesToDb(Session)
mailing = MailingEngine(queries_to_db)


def send_keyboard_with_mailing_type_for_admin(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, "Выберите тип рассылки:",
                     reply_markup=keyboard_with_mailing_type_for_admin())


def process_answer_for_new_admin_mailing_with_photo(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Пришлите фото для рассылки")
        bot.register_next_step_handler(call.message, process_save_photo_for_new_mailing)

    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_answer_for_new_mailing_without_photo_as_admin(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)

        bot.send_message(call.message.chat.id, "Пришлите описание для рассылки")
        bot.register_next_step_handler(call.message, process_save_description_for_new_mailing_as_admin)

    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def process_save_photo_for_new_mailing(message):
    try:
        bot.delete_message(message.chat.id, message.id)

        photo = message.photo[-1]
        file_id = photo.file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        file_name = generate_key(7)

        with open(f'beauty_bot/app/photos/{file_name}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        mailing.url_to_photo = file_name + '.jpg'

        bot.send_message(message.chat.id, "Пришлите описание для рассылки")

        bot.register_next_step_handler(message, process_save_description_for_new_mailing_as_admin)
    except Exception as e:
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды(")


def process_save_description_for_new_mailing_as_admin(message):

    bot.delete_message(message.chat.id, message.id - 1)
    bot.delete_message(message.chat.id, message.id)

    mailing.description = message.text

    bot.send_message(message.chat.id, 'Выберите город для рассылки',
                     reply_markup=keyboard_with_cities_for_admin_mailing())


def process_save_city_for_new_mailing_as_admin(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    mailing.city = call.data[len('ad_ml_c'):]

    bot.send_message(call.message.chat.id, "Выберите район для рассылки",
                     reply_markup=keyboard_with_districts_for_admin_mailing(call.data))


def process_save_area_for_new_mailing_as_admin(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    mailing.district = call.data[len('ad_ml_dist_'):]

    bot.send_message(call.message.chat.id, 'Управление рассылкой', reply_markup=keyboard_to_srart_mailing_for_amdin())


def start_mailing_as_admin(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    mailing.fill_users()
    mailing.start_mailing(call.message.chat.id, bot)

    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


