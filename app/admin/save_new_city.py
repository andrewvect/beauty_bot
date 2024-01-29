import traceback

from ..apps_tools.message_deleter import delete_previous_messages
from ..db_queries import check_if_city_exist, add_new_city
from beauty_bot.extantions import bot
from ..keyboards import admin_keyboard2

selected_area = ''


@delete_previous_messages
def handle_button2_click(call):
    bot.send_message(call.message.chat.id, "Напишите название города:")

    bot.register_next_step_handler(call.message, process_save_new_city)


@delete_previous_messages
def process_save_new_city(message):

    if check_if_city_exist(message.text):
        bot.send_message(message.chat.id, f'Данный город уже существует')
    else:
        bot.send_message(message.chat.id, f'Город "{message.text.capitalize()}" успешно создан')
        add_new_city(message.text)

    bot.send_message(message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
