from telebot import types

from beauty_bot.extantions import bot


def send_menu_with_photo(call, type, menu, keyboard, message):
    with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(call.message.chat.id,
                       caption=message,
                       photo=photo,
                       reply_markup=keyboard(menu, type))


def edit_message(call, menu, keyboard, message, type):

    edit_menu_with_photo(call, type, menu, keyboard)
    edit_message_caption(call, menu, keyboard, message, type)


def edit_menu_with_photo(call, type, menu, keyboard):
    with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo),
                               chat_id=call.message.chat.id,
                               message_id=call.message.id,
                               reply_markup=keyboard(menu, type))


def edit_message_caption(call, menu, keyboard, message, type):
    bot.edit_message_caption(caption=message, chat_id=call.message.chat.id,
                             message_id=call.message.id,
                             reply_markup=keyboard(menu, type))