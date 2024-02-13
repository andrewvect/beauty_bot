from beauty_bot.app.admin.tools import send_menu_with_photo, edit_message
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.keyboards.keyboards import menu_with_questionaries, admin_keyboard2, menu_with_questionaries_search_by_city


def create_message_for_questionary(menu):
    message = f"{menu.masted_data['description']} \n" \
              f"Город: {menu.city_name.capitalize()} \n" \
              f"Район города: {menu.city_name.capitalize()} \n"

    return message


def send_menu_with_questionaries(call, type, state, menu):
    try:

        menu.get_data_for_questionary()

        if state == 'new':
            send_menu_with_photo(call, type, menu, menu_with_questionaries, create_message_for_questionary(menu))

        if state == 'old':
            edit_message(call, menu, menu_with_questionaries, create_message_for_questionary(menu), type)

    except Exception:
        bot.send_message(call.message.chat.id, "Не создано еще ни одной анкеты.")
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())


def send_menu_by_type(call, state, type_master, menu):
    if state == 'new':
        send_menu_with_photo(call, type_master, menu,
                             menu_with_questionaries_search_by_city(menu, type_master), menu.get_description())

    if state == 'old':
        edit_message(call, menu, menu_with_questionaries_search_by_city(menu, type_master),
                     menu.get_description(), type_master)
