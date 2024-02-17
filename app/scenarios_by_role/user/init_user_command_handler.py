from beauty_bot.app.app_tools.db_queries import db
from beauty_bot.app.scenarios_by_role.user import user_masters_menu
from beauty_bot.extantions import bot


def handle_start_command(message):
    db.add_user_to_database(message.chat.id)

    referral_link = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

    user_has_subscriptions = db.get_user_subscriptions(message.chat.id)

    if not referral_link and not user_has_subscriptions:
        with open(f"beauty_bot/app/photos/title.jpg", 'rb') as photo:
            bot.send_photo(message.chat.id, photo,
                           caption='Чтобы пользоваться сервисом onebeauty - запустите его по реферальной ссылке мастера.')

    if referral_link:
        bot.reply_to(message, f"Вы использовали реферальную ссылку: {referral_link}")
        user_masters_menu.subscribe_on_master(message, referral_link)

    user_masters_menu.send_menu_with_questionarties_masters(message)

