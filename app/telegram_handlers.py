import logging
import traceback

from beauty_bot.app.scenarios_by_role.admin.admin_authorization import handle_admin_login
from beauty_bot.app.app_tools.services import is_login_command
from beauty_bot.extantions import bot
from beauty_bot.app.app_tools.logger.logger import log_error
from beauty_bot.app.scenarios_by_role.user.init_user_command_handler import handle_start_command


@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.info(f"start command from user id:{message.chat.id}, username:{message.from_user.username}")
    try:
        handle_start_command(message)
    except Exception as e:
        traceback.print_exc()
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды :(")


@bot.message_handler(func=is_login_command)
def handle_start(message):
    logging.info(f"login command from user id:{message.chat.id}, username:{message.from_user.username} as admin")
    try:
        handle_admin_login(message)
    except Exception as e:
        traceback.print_exc()
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды login:(")


if __name__ == '__main__':
    bot.polling(none_stop=True)
