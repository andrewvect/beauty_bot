import traceback

from telebot import types
from beauty_bot.extantions import bot
from beauty_bot.app.keyboards import menu_with_questionaries, admin_keyboard2


def send_menu_with_questionaries(call, type, state, menu):
    try:

        menu.get_data_for_questionary()
        data = menu.master_data

        message = f"{data['description']} \n" \
                  f"Город: {menu.city_name.capitalize()} \n" \
                  f"Район города: {menu.city_name.capitalize()} \n"

        if state == 'new':
            with open(f"beauty_bot/app/photos/{data['url_to_photo']}.jpg", 'rb') as photo:
                bot.send_photo(call.message.chat.id,
                               caption=message,
                               photo=photo,
                               reply_markup=menu_with_questionaries(data['is_active'],
                                                                    menu.count_numbers(),
                                                                    type,
                                                                    data['id']))

        if state == 'old':
            try:
                with open(f"beauty_bot/app/photos/{data['url_to_photo']}.jpg", 'rb') as photo:

                    bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                                           chat_id=call.message.chat.id,
                                           message_id=call.message.id,
                                           reply_markup=menu_with_questionaries(data['is_active'],
                                                                                menu.count_numbers(), type,
                                                                                data['id']))

            except Exception:
                print(traceback.print_exc())
            try:

                bot.edit_message_caption(caption=message, chat_id=call.message.chat.id, message_id=call.message.id,
                                         reply_markup=menu_with_questionaries(data['is_active'],
                                                                              menu.count_numbers(), type,
                                                                              data['id']))
            except Exception:
                print(traceback.print_exc())

    except Exception:
        print(traceback.print_exc())
        bot.send_message(call.message.chat.id, "Не создано еще ни одной анкеты.")
        bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboard2())