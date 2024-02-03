from beauty_bot.app.apps_tools.message_deleter import delete_previous_messages
from beauty_bot.app.db_queries import get_city_id_by_name, check_if_area_exist, add_new_area
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import admin_keyboard2, keyboard_with_towns

selected_area = ''


@delete_previous_messages
def process_ckeck_city(message):
    global selected_area
    selected_area = message.text.lower()

    bot.send_message(message.chat.id, "Доступные города", reply_markup=keyboard_with_towns())


@delete_previous_messages
def handle_button3_click(call):
    bot.send_message(call.message.chat.id, "Напишите название района города:")


@delete_previous_messages
def handle_save_area_town(call):
    city_id = get_city_id_by_name(call.data[5:])

    global selected_area
    if check_if_area_exist(selected_area, city_id):
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" уже существует в городе "{call.data[5:].capitalize()}"')
    else:
        add_new_area(city_id, selected_area)
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" успешно добавлен для города "{call.data[5:].capitalize()}"')

    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
