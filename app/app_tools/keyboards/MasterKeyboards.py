from beauty_bot.app.app_tools.keyboards.Base import BaseKeyboards
from beauty_bot.app.app_tools.keyboards.CallBackButtons import MasterCallBackButtons


class MasterKeyboards(BaseKeyboards, MasterCallBackButtons):

    def keyboard_to_start_mailing_as_master(self):
        return super().keyboard_to_start_mailing(self.button_to_start_mailing, self.button_to_return_to_menu)

    def keyboard_master_menu(self):
        return super().keyboard_to_start_mailing(self.button_open_mailing, self.button_out_of_mailing)

    def keyboard_with_mailing_as_master(self):
        return super().keyboard_mailing(self.button_mailing_with_photo, self.button_mailing_without_photo)


master_keyboards = MasterKeyboards()
