
from unittest import skip

from beauty_bot.app.tests.base import Base
from beauty_bot.app.tools import MailingEngine, QueriesToDb


class TestQueriesToDbClass(Base):

    def test_fill_users_with_city_function(self):

        db_class = QueriesToDb(self.Session)
        mailing = MailingEngine(db_class)

        mailing.city = 'City1'
        mailing.fill_users()

        self.assertCountEqual(mailing.users, [789, 999])

    def test_fill_users_with_district_function(self):

        db_class = QueriesToDb(self.Session)
        mailing = MailingEngine(db_class)

        mailing.city = 'City2'
        mailing.district = 'Area2'
        mailing.fill_users()

        self.assertCountEqual(mailing.users, [101])

