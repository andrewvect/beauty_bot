from beauty_bot.app.app_tools.keyboards.AdminKeyboards import admin_keyboards
from beauty_bot.app.config import CONFIG
from beauty_bot.app.scenarios_by_role.master import master_menu
from beauty_bot.extantions import bot

admin_id = []


def handle_admin_login(message):

    message_text = message.text.lower().split()
    if message_text[1] == CONFIG.admin_key:

        if message.chat.id not in admin_id:
            admin_id.append(message.chat.id)

        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "Меню админа:", reply_markup=admin_keyboards.admin_keyboard2())

    else:
        if master_menu.check_master_key(message.from_user.username, message_text[1]):
            master_menu.send_keyboard_with_master_menu(message)
        else:
            bot.send_message(message.chat.id, 'Ошибка авторизации')
