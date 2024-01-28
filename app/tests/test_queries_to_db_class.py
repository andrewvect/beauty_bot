from unittest import skip

from beauty_bot.app.tests.base import Base
from beauty_bot.app.tools import QueriesToDb


class TestQueriesToDbClass(Base):

    def test_all_users_by_district(self):

        db_class = QueriesToDb(self.Session)

        self.assertCountEqual([999, 789], db_class.all_users_by_district('Area1', 'City1'))
        self.assertCountEqual([101], db_class.all_users_by_district('Area2','City2'))
        self.assertCountEqual([], db_class.all_users_by_city('Area3'))
        self.assertCountEqual([], db_class.all_users_by_city(''))

    def test_all_users_by_city(self):

        db_class = QueriesToDb(self.Session)

        self.assertCountEqual([999, 789], db_class.all_users_by_city('City1'))
        self.assertCountEqual([101], db_class.all_users_by_city('City2'))
        self.assertCountEqual([], db_class.all_users_by_city('City3'))

    def test_all_partners_by_city_id(self):

        db_class = QueriesToDb(self.Session)

        self.assertEqual([3], db_class.all_partners_by_area_id(1))
        self.assertEqual([4], db_class.all_partners_by_area_id(2))
        self.assertEqual([], db_class.all_partners_by_area_id(3))

    def test_get_all_user_signed_masters_id_with_user_by_id(self):

        db_class = QueriesToDb(self.Session)

        self.assertEqual([2, 1], db_class.get_all_user_signed_masters_id_with_user_by_id(1001))
        self.assertEqual([1], db_class.get_all_user_signed_masters_id_with_user_by_id(999))

    def test_master_ids_by_city_name(self):
        db_class = QueriesToDb(self.Session)
        self.assertEqual([1 ], db_class.get_all_masters_id_by_city_name('City1'))

    def test_partners_ids_by_city_name(self):
        db_class = QueriesToDb(self.Session)
        self.assertEqual([3], db_class.get_all_partners_id_by_city_name('City1'))
        self.assertEqual([4], db_class.get_all_partners_id_by_city_name('City2'))






