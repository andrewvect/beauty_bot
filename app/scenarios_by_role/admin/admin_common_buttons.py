from beauty_bot.app.app_tools.message_deleter import delete_previous_messages
from beauty_bot.app.app_tools.keyboards.AdminKeyboards import admin_keyboards
from beauty_bot.extantions import bot


@delete_previous_messages
def admin_logout(call) -> None:
    pass


@delete_previous_messages
def return_to_admin_menu(call):
    bot.send_message(call.message.chat.id, "Меню админа", reply_markup=admin_keyboards.admin_keyboard2())
