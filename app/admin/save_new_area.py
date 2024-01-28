
from beauty_bot.app.db_queries import get_city_id_by_name, check_if_area_exist, add_new_area
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import admin_keyboard2, keyboard_with_towns
from beauty_bot.app.logger import log_error


def process_ckeck_city(message):
    global selected_area
    selected_area = message.text.lower()

    bot.delete_message(message.chat.id, message.id)
    bot.delete_message(message.chat.id, message.id - 1)

    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns())


def handle_button3_click(call):
    try:
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(call.message.chat.id, "Напишите название района города:")
        bot.register_next_step_handler(call.message, process_ckeck_city)

    except Exception as e:
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды")


def handle_save_area_town(call):
    bot.delete_message(call.message.chat.id, call.message.id)

    city_id = get_city_id_by_name(call.data[5:])

    if check_if_area_exist(selected_area, city_id):
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" уже существует в городе "{call.data[5:].capitalize()}"')
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
    else:
        add_new_area(city_id, selected_area)
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" успешно добавлен для города "{call.data[5:].capitalize()}"')
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())