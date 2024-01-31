from telebot import types

from beauty_bot.extantions import bot


def send_menu_with_photo(call, type, menu, keyboard, message):
    with open(f"beauty_bot/app/photos/{menu.master_data['url_to_photo']}.jpg", 'rb') as photo:
        bot.send_photo(call.message.chat.id,
                       caption=message,
                       photo=photo,
                       reply_markup=keyboard(menu, type))


def create_message_with_successful_save_new_master(master_state, api_key, referal_key, CONFIG) -> str:

    if master_state['is_partner']:
        value = 'партнера'
    else:
        value = 'мастера'

    message = f"Анкета {value} {master_state['username']} создана!\n"
    f"Api key: {api_key} \n"
    f"Referal link: https://t.me/{CONFIG.bot_name_tg[1:]}?start={referal_key}"
    return message


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
