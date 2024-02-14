from beauty_bot.app.app_tools.keyboards.Base import BaseKeyboards


class MasterKeyboards(BaseKeyboards):

    def keyboard_to_start_mailing_as_master(self):
        return super().keyboard_to_start_mailing('start_mailing', 'return_to_master_menu')

    def keyboard_master_menu(self):
        return super().keyboard_to_start_mailing('mailing', 'out_as_ms')

    def keyboard_with_mailing_as_master(self):
        return super().keyboard_mailing('mailing_with_photo', 'mailing_without_photo')


master_keyboards = MasterKeyboards()