import traceback

from beauty_bot.app.search_engine import profiles_masters_by_city, send_cites_to_find_masters_profiles, \
    next_page_admin_partner_menu_by_city, \
    previous_page_admin_master_menu_by_city, profiles_partners_by_city, send_cites_to_find_partners_profiles, \
    next_page_admin_master_menu_by_city, previous_page_admin_partner_menu_by_city, \
    change_master_visibility_in_find_menu, change_partner_visibility_in_find_menu
from services import is_login_command, admin_keyboard2, process_choose_type_master, handle_button2_click, \
    handle_button3_click, handle_save_area_town, handle_save_new_master_town, handle_save_new_master, \
    handle_master_type_click, back_to_admin_menu_from_questionaries, next_page_masters_admin_menu, \
    previous_page_masters_admin_menu, send_menu_with_partners, send_menu_with_masters, \
    admin_logout, send_keyboard_with_mailing_type, send_keyboard_with_master_menu, \
    process_answer_for_new_mailing_with_photo, start_mailing, \
    check_master_key, subscribe_on_master, process_answer_for_new_mailing_without_photo, send_user_menu, \
    next_page_user_menu, previous_page_user_menu, send_master_url_to_telegram, send_master_url_to_portfolio, \
    send_master_url_to_reviews, send_keyboard_with_partners, next_page_user_partners_menu, \
    previous_page_user_partners_menu, change_master_visibility, change_partner_visibility, \
    next_page_partners_admin_menu, previous_page_partners_admin_menu, send_master_profile_by_referall_link
from config import admin_key
from extantions import bot

admin_id = []


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        referral_link = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

        if referral_link:
            bot.reply_to(message, f"Вы использовали реферральную ссылку: {referral_link}")
            send_master_profile_by_referall_link(message, referral_link)
            subscribe_on_master(message.chat.id, referral_link)
        else:
            send_user_menu(message)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка обработки комманды(")


# Обработчик команды /login
@bot.message_handler(func=is_login_command)
def handle_start(message):
    try:
        message_text = message.text.lower().split()
        if message_text[1] == admin_key:
            if message.chat.id in admin_id:
                pass
            else:
                admin_id.append(message.chat.id)
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, "Меню админа:", reply_markup=admin_keyboard2())
        else:
            if check_master_key(message.from_user.username, message_text[1]):
                send_keyboard_with_master_menu(message)
            else:
                bot.send_message(message.chat.id, 'Ошибка авторизации')

    except Exception as e:
        traceback.print_exc()
        bot.send_message(message.chat.id, "Ошибка обработки комманды login")


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    try:
        if call.data.startswith('type_'):
            process_choose_type_master(call)
        if call.data == 'button2':
            handle_button2_click(call)
        if call.data == 'button3':
            handle_button3_click(call)
        if call.data.startswith('town_'):
            handle_save_area_town(call)
        if call.data.startswith('save_new_master_town_'):
            handle_save_new_master_town(call)
        if call.data.startswith('save_new_master_area_'):
            handle_save_new_master(call)
        if call.data.startswith('chose'):
            handle_master_type_click(call)
        if call.data == 'partners_questionnaires':
            send_menu_with_partners(call)
        if call.data == 'masters_questionnaires':
            send_menu_with_masters(call)
        if call.data == 'back_menu':
            back_to_admin_menu_from_questionaries(call)
        if call.data.startswith('ad_next_page_masters'):
            next_page_masters_admin_menu(call)
        if call.data == 'ad_previous_page_masters':
            previous_page_masters_admin_menu(call)
        if call.data.startswith('ad_next_page_partners'):
            next_page_partners_admin_menu(call)
        if call.data == 'ad_previous_page_partners':
            previous_page_partners_admin_menu(call)
        if call.data == 'logout':
            admin_logout(call)
        if call.data == 'mailing':
            send_keyboard_with_mailing_type(call)
        if call.data == 'mailing_with_photo':
            process_answer_for_new_mailing_with_photo(call)
        if call.data == 'mailing_without_photo':
            process_answer_for_new_mailing_without_photo(call)
        if call.data == 'start_mailing':
            start_mailing(call)
        if call.data == 'return_to_master_menu':
            send_keyboard_with_master_menu(call.message)
        if call.data == 'next_user_menu_':
            next_page_user_menu(call)
        if call.data == 'previous_user_menu_':
            previous_page_user_menu(call)
        if call.data.startswith('ms_cont_'):
            send_master_url_to_telegram(call)
        if call.data.startswith('ms_port_'):
            send_master_url_to_portfolio(call)
        if call.data.startswith('ms_reviews_'):
            send_master_url_to_reviews(call)
        if call.data == ('partners'):
            send_keyboard_with_partners(call.message)
        if call.data == 'previous_partn_menu_':
            previous_page_user_partners_menu(call)
        if call.data == 'next_partn_menu_':
            next_page_user_partners_menu(call)
        if call.data == 'back_us_menu':
            send_user_menu(call.message)
        if call.data.startswith('acv_M'):
            change_master_visibility(call)
        if call.data.startswith('acv_P'):
            change_partner_visibility(call)

        if call.data.startswith('acvF_M'):
            change_master_visibility_in_find_menu(call)
        if call.data.startswith('acvF_P'):
            change_partner_visibility_in_find_menu(call)

        if call.data.startswith('search_as_adminM'):
            send_cites_to_find_masters_profiles(call)
        if call.data.startswith('search_as_adminP'):
            send_cites_to_find_partners_profiles(call)
        if call.data.startswith('fM_'):
            profiles_masters_by_city(call)
        if call.data.startswith('fP_'):
            profiles_partners_by_city(call)
        if call.data == 'ad_f_next_ct_masters':
            next_page_admin_master_menu_by_city(call)
        if call.data == 'ad_f_previous_ct_masters':
            previous_page_admin_master_menu_by_city(call)
        if call.data == 'ad_f_next_ct_partners':
            next_page_admin_partner_menu_by_city(call)
        if call.data == 'ad_f_previous_ct_partners':
            previous_page_admin_partner_menu_by_city(call)

    except Exception as e:
        traceback.print_exc()
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды(")


if __name__ == '__main__':
    bot.polling(none_stop=True)
