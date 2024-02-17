from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.AdminKeyboards import admin_keyboards

selected_area = ''


@delete_previous_messages
def process_ckeck_city(message):
    global selected_area
    selected_area = message.text.lower()

    bot.send_message(message.chat.id, "Доступные города", reply_markup=admin_keyboards.keyboard_with_towns())


@delete_previous_messages
def handle_button3_click(call):
    bot.send_message(call.message.chat.id, "Напишите название района города:")
    bot.register_next_step_handler(call.message, process_ckeck_city)


@delete_previous_messages
def handle_save_area_town(call):
    city_id = db.get_city_id_by_name(call.data[5:])

    global selected_area
    if db.check_if_area_exist(selected_area, city_id):
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" уже существует в городе "{call.data[5:].capitalize()}"')
    else:
        db.add_new_area(city_id, selected_area)
        bot.send_message(call.message.chat.id,
                         f'Район "{selected_area.capitalize()}" успешно добавлен для города "{call.data[5:].capitalize()}"')

    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboards.admin_keyboard2())
