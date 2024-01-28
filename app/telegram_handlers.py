
import traceback

from beauty_bot.app.admin.admin_mailing_engine import process_answer_for_new_admin_mailing_with_photo, \
    send_keyboard_with_mailing_type_for_admin, \
    process_answer_for_new_mailing_without_photo_as_admin, start_mailing_as_admin, \
    process_save_city_for_new_mailing_as_admin, process_save_area_for_new_mailing_as_admin
from beauty_bot.app.admin.menu_with_masters import \
     send_menu_with_masters, back_to_admin_menu_from_questionaries, \
     next_page_masters_admin_menu, previous_page_masters_admin_menu,  \
     admin_logout, change_master_visibility
from beauty_bot.app.admin.menu_with_partners import send_menu_with_partners, next_page_partners_admin_menu, \
    previous_page_partners_admin_menu, change_partner_visibility
from beauty_bot.app.admin.save_new_area import handle_button3_click, handle_save_area_town
from beauty_bot.app.admin.save_new_city import handle_button2_click
from beauty_bot.app.admin.save_new_master_or_partner import process_choose_type_master, handle_save_new_master_town, \
    handle_save_new_master, handle_master_type_click
from beauty_bot.app.admin.search_engine_partners import change_partner_visibility_in_find_menu, \
    send_cites_to_find_partners_profiles, profiles_partners_by_city, next_page_admin_partner_menu_by_city, \
    previous_page_admin_partner_menu_by_city
from beauty_bot.app.db_queries import add_user_to_database
from beauty_bot.app.keyboards import admin_keyboard2
from beauty_bot.app.master.master_menu import check_master_key, send_keyboard_with_master_menu, \
    send_keyboard_with_mailing_type, process_answer_for_new_mailing_with_photo, \
    process_answer_for_new_mailing_without_photo, start_mailing
from beauty_bot.app.user.user_masters_menu import subscribe_on_master, send_menu_with_questionarties_masters, next_page_user_menu, \
    previous_page_user_menu, send_menu_with_questionarties_masters2
from beauty_bot.app.admin.search_engine_masters import profiles_masters_by_city, send_cites_to_find_masters_profiles, \
    change_master_visibility_in_find_menu, next_page_admin_master_menu_by_city, previous_page_admin_master_menu_by_city
from beauty_bot.app.user.user_partners_menu import process_partners_menu, previous_page_user_partners_menu, \
    next_page_user_partners_menu
from services import is_login_command
from config import admin_key
from beauty_bot.extantions import bot
from logger import log_error

admin_id = []


@bot.message_handler(commands=['start'])
def handle_start(message):

    add_user_to_database(message.chat.id)
    try:
        referral_link = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None

        if referral_link:
            bot.reply_to(message, f"Вы использовали реферральную ссылку: {referral_link}")
            subscribe_on_master(message, referral_link)
        else:
            try:
                send_menu_with_questionarties_masters(message)
            except Exception:
                with open(f"beauty_bot/app/photos/title.jpg", 'rb') as photo:
                    bot.send_photo(message.chat.id, photo,
                                   caption='Чтобы пользоваться сервисом onebeauty - запустите его по реферальной ссылке мастера.')

    except Exception as e:
        traceback.print_exc()
        log_error(e)
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
        log_error(e)
        bot.send_message(message.chat.id, "Ошибка обработки комманды login")


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    print(call.data)
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
        if call.data.startswith('partners_mn_'):
            process_partners_menu(call)
        if call.data == 'previous_partn_menu_':
            previous_page_user_partners_menu(call)
        if call.data == 'next_partn_menu_':
            next_page_user_partners_menu(call)
        if call.data == 'back_us_menu':
            send_menu_with_questionarties_masters2(call.message)
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
        if call.data == 'ad_f_next_M':
            next_page_admin_master_menu_by_city(call)
        if call.data == 'ad_f_previous_M':
            previous_page_admin_master_menu_by_city(call)
        if call.data == 'ad_f_next_P':
            next_page_admin_partner_menu_by_city(call)
        if call.data == 'ad_f_previous_P':
            previous_page_admin_partner_menu_by_city(call)
        if call.data == 'admin_mailing':
            send_keyboard_with_mailing_type_for_admin(call)
        if call.data == 'ad_ml_w_photo':
            process_answer_for_new_admin_mailing_with_photo(call)
        if call.data == 'ad_ml_wiout_photo':
            process_answer_for_new_mailing_without_photo_as_admin(call)
        if call.data.startswith('ad_ml_c'):
            process_save_city_for_new_mailing_as_admin(call)
        if call.data.startswith('ad_ml_dist_'):
            process_save_area_for_new_mailing_as_admin(call)
        if call.data == 'start_ml_ad':
            start_mailing_as_admin(call)
        if call.data == 'return_to_admin_menu':
            start_mailing_as_admin(call)

    except Exception as e:
        traceback.print_exc()
        log_error(e)
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды(")


if __name__ == '__main__':
    bot.polling(none_stop=True)
