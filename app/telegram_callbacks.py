import traceback

from beauty_bot.app.scenarios_by_role.admin.admin_common_buttons import back_to_admin_menu_from_questionaries, \
    admin_logout
import beauty_bot.app.scenarios_by_role.admin.admin_mailing_engine as admin_mailing_engine
import beauty_bot.app.scenarios_by_role.admin.menu_with_masters as menu_with_masters
import beauty_bot.app.scenarios_by_role.admin.menu_with_partners as menu_with_partners
from beauty_bot.app.scenarios_by_role.admin.save_new_area import handle_button3_click, handle_save_area_town
import beauty_bot.app.scenarios_by_role.admin.save_new_master_or_partner as save_new_master_or_partner
import beauty_bot.app.scenarios_by_role.admin.search_engine_partners as search_engine_partners
import beauty_bot.app.scenarios_by_role.master.master_menu as master_menu
import beauty_bot.app.scenarios_by_role.user.user_masters_menu as user_masters_menu
import beauty_bot.app.scenarios_by_role.admin.search_engine_masters as search_engine_masters
import beauty_bot.app.scenarios_by_role.user.user_partners_menu as user_partners_menu
from beauty_bot.app.app_tools.keyboards.CallBackButtons import MasterCallBackButtons, AdminCallBackButtons, \
    UserCallBackButtons
from beauty_bot.app.app_tools.logger.logger import log_error
from beauty_bot.app.scenarios_by_role.admin.save_new_city import handle_button2_click
from beauty_bot.extantions import bot


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    try:
        if call.data.startswith(AdminCallBackButtons.create_questionary):
            save_new_master_or_partner.process_choose_type_master(call)

        elif call.data == AdminCallBackButtons.add_city:
            handle_button2_click(call)

        elif call.data == AdminCallBackButtons.add_district:
            handle_button3_click(call)

        elif call.data.startswith('town_'):
            handle_save_area_town(call)

        elif call.data.startswith(AdminCallBackButtons.save_new_master_town):
            save_new_master_or_partner.handle_save_new_master_town(call)

        elif call.data.startswith(AdminCallBackButtons.save_new_master_area):
            save_new_master_or_partner.handle_save_new_master(call)

        elif call.data.startswith('chose'):
            save_new_master_or_partner.handle_master_type_click(call)

        elif call.data == AdminCallBackButtons.partners_questionnaires:
            menu_with_partners.send_menu_with_partners(call)

        elif call.data == AdminCallBackButtons.masters_questionnaires:
            menu_with_masters.send_menu_with_masters(call)

        elif call.data == 'back_menu':
            back_to_admin_menu_from_questionaries(call)

        elif call.data.startswith('ad_next_page_masters'):
            menu_with_masters.next_page_masters_admin_menu(call)

        elif call.data == 'ad_previous_page_masters':
            menu_with_masters.previous_page_masters_admin_menu(call)

        elif call.data.startswith('ad_next_page_partners'):
            menu_with_partners.next_page_partners_admin_menu(call)

        elif call.data == 'ad_previous_page_partners':
            menu_with_partners.previous_page_partners_admin_menu(call)

        elif call.data == AdminCallBackButtons.logout:
            admin_logout(call)

        elif call.data == MasterCallBackButtons.button_open_mailing:
            master_menu.send_keyboard_with_mailing_type(call)

        elif call.data == MasterCallBackButtons.button_mailing_with_photo:
            master_menu.process_answer_for_new_mailing_with_photo(call)

        elif call.data == MasterCallBackButtons.button_mailing_without_photo:
            master_menu.process_answer_for_new_mailing_without_photo(call)

        elif call.data == MasterCallBackButtons.button_to_start_mailing:
            master_menu.start_mailing(call)

        elif call.data == MasterCallBackButtons.button_to_return_to_menu:
            master_menu.send_keyboard_with_master_menu(call.message)

        elif call.data == UserCallBackButtons.button_next_master_questionnaire:
            user_masters_menu.next_page_user_menu(call)

        elif call.data == UserCallBackButtons.button_previous_master_questionnaire:
            user_masters_menu.previous_page_user_menu(call)

        elif call.data.startswith(UserCallBackButtons.button_show_master_partners):
            user_partners_menu.process_partners_menu(call)

        elif call.data == UserCallBackButtons.button_previous_partner_questionnaire:
            user_partners_menu.previous_page_user_partners_menu(call)

        elif call.data == UserCallBackButtons.button_next_partner_questionnaire:
            user_partners_menu.next_page_user_partners_menu(call)

        elif call.data == UserCallBackButtons.button_back_to_master_menu:
            user_masters_menu.send_menu_with_questionarties_masters2(call.message)

        elif call.data.startswith('acv_M'):
            menu_with_masters.change_master_visibility(call)

        elif call.data.startswith('acv_P'):
            menu_with_partners.change_partner_visibility(call)

        elif call.data.startswith(AdminCallBackButtons.button_change_status + 'M'):
            search_engine_masters.change_master_visibility_in_find_menu(call)

        elif call.data.startswith(AdminCallBackButtons.button_change_status + 'P'):
            search_engine_partners.change_partner_visibility_in_find_menu(call)

        elif call.data.startswith(AdminCallBackButtons.search_button + 'M'):
            search_engine_masters.send_cites_to_find_masters_profiles(call)

        elif call.data.startswith(AdminCallBackButtons.search_button + 'P'):
            search_engine_partners.send_cites_to_find_partners_profiles(call)

        elif call.data.startswith('fM_'):
            search_engine_masters.profiles_masters_by_city(call)

        elif call.data.startswith('fP_'):
            search_engine_partners.profiles_partners_by_city(call)

        elif call.data == AdminCallBackButtons.button_next + 'M':
            search_engine_masters.next_page_admin_master_menu_by_city(call)

        elif call.data == AdminCallBackButtons.button_previous + 'M':
            search_engine_masters.previous_page_admin_master_menu_by_city(call)

        elif call.data == AdminCallBackButtons.button_next + 'P':
            search_engine_partners.next_page_admin_partner_menu_by_city(call)

        elif call.data == AdminCallBackButtons.button_previous + 'P':
            search_engine_partners.previous_page_admin_partner_menu_by_city(call)

        elif call.data == AdminCallBackButtons.admin_mailing:
            admin_mailing_engine.send_keyboard_with_mailing_type_for_admin(call)

        elif call.data == AdminCallBackButtons.mailing_with_photo:
            admin_mailing_engine.process_answer_for_new_admin_mailing_with_photo(call)

        elif call.data == AdminCallBackButtons.mailing_without_photo:
            admin_mailing_engine.process_answer_for_new_mailing_without_photo_as_admin(call)

        elif call.data.startswith(AdminCallBackButtons.button_with_cities):
            admin_mailing_engine.process_save_city_for_new_mailing_as_admin(call)

        elif call.data.startswith(AdminCallBackButtons.button_with_districts):
            admin_mailing_engine.process_save_area_for_new_mailing_as_admin(call)

        elif call.data == AdminCallBackButtons.start_mailing:
            admin_mailing_engine.start_mailing_as_admin(call)

        elif call.data == AdminCallBackButtons.return_to_admin_menu:
            admin_mailing_engine.start_mailing_as_admin(call)

    except Exception as e:
        traceback.print_exc()
        log_error(f"Ooops! Error: {e}")
        bot.send_message(call.message.chat.id, "Ошибка обработки комманды(")
