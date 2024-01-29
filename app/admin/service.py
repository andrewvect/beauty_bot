import traceback

from telebot import types
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import menu_with_questionaries, admin_keyboard2


def create_message_for_questionary(menu):
    message = f"{menu.masted_data['description']} \n" \
              f"Город: {menu.city_name.capitalize()} \n" \
              f"Район города: {menu.city_name.capitalize()} \n"

    return message


def send_menu_with_photo(call, type, menu):
    with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(call.message.chat.id,
                       caption=create_message_for_questionary(menu),
                       photo=photo,
                       reply_markup=menu_with_questionaries(menu, type))


def edit_menu_with_photo(call, type, menu):
    with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.id,
                               reply_markup=menu_with_questionaries(menu, type))


def edit_message_caption(call, menu):
    bot.edit_message_caption(caption=create_message_for_questionary(menu), chat_id=call.message.chat.id,
                             message_id=call.message.id,
                             reply_markup=menu_with_questionaries(menu, type))


def send_menu_with_questionaries(call, type, state, menu):
    try:

        menu.get_data_for_questionary()

        if state == 'new':
            send_menu_with_photo(call, type, menu)

        if state == 'old':
            try:
                edit_menu_with_photo(call, type, menu)

            except Exception:
                pass

            try:

                edit_message_caption(call, menu)

            except Exception:
                pass

    except Exception:
        bot.send_message(call.message.chat.id, "Не создано еще ни одной анкеты.")
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())
