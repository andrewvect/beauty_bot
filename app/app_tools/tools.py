from sqlalchemy.orm import aliased
from abc import abstractmethod

from models import CityAreaModel, UserModel, MasterModel, CityModel, user_master_association


class QueriesToDb:

    def __init__(self, session):
        self.session = session()

    def all_users_by_district(self, area_name: str, city_name: str) -> list:
        with self.session as session:
            city_instance = session.query(CityModel).filter_by(name=city_name).first()
            city_area = session.query(CityAreaModel).filter_by(name=area_name, city_id=city_instance.id).first()

            if city_area:

                masters_in_area = city_area.masters

                user_telegram_ids = []
                for master in masters_in_area:
                    users_of_master = master.users
                    for user in users_of_master:
                        user_telegram_ids.append(user.telegram_id)

                return user_telegram_ids
            else:
                return []

    def all_users_by_city(self, city_name: str) -> list:
        with self.session as session:
            city = session.query(CityModel).filter_by(name=city_name).first()

            if city:
                users_in_city = session.query(UserModel).join(MasterModel, UserModel.masters).filter(
                    MasterModel.areas.has(city=city)).all()

                telegram_ids = [user.telegram_id for user in users_in_city]
                return telegram_ids
            else:
                return []

    def get_city_id_by_area_id(self, area_id) -> int:
        with self.session as session:
            city_id = (
                session.query(CityModel.id)
                    .join(CityAreaModel, CityModel.areas)
                    .filter(CityAreaModel.id == area_id)
                    .scalar()
            )
        return city_id

    def all_partners_by_area_id(self, area_id: int) -> list:
        with self.session as session:
            partners = (
                session.query(MasterModel)
                    .join(CityAreaModel, MasterModel.location_id == CityAreaModel.id)
                    .filter(MasterModel.is_partner == True)
                    .filter(CityAreaModel.id == area_id)
                    .all()
            )
        partners_ids = [partner.id for partner in partners if partner.is_active]
        return partners_ids

    def get_data_for_master_questionary_by_id(self, master_id: int) -> dict:
        with self.session as session:
            master = session.query(MasterModel).filter_by(id=master_id).first()
            return {'id': master.id,
                    'telegram_user_name': master.telegram_user_name,
                    'key': master.key,
                    'referal_link': master.referal_link,
                    'description': master.description,
                    'username': master.username,
                    'url_to_photo': master.url_to_photo,
                    'is_partner': master.is_partner,
                    'is_active': master.is_active,
                    'location_id': master.location_id,
                    'reviews_url': master.reviews_url,
                    'master_portfolio_url': master.master_portfolio_url,
                    }

    def get_ids_masters_by_type(self, user_telegram_id: int, type: bool):
        with self.session as session:
            user = session.query(UserModel).filter_by(telegram_id=user_telegram_id).first()
            master_ids = [master.id for master in user.masters if master.is_partner is type and master.is_active]
            return master_ids

    def get_all_user_signed_masters_id_with_user_by_id(self, user_telegram_id) -> list:
        masters_ids = self.get_ids_masters_by_type(user_telegram_id, False)
        return masters_ids

    def get_master_id_by_referral_url(self, ref_url) -> int:
        with self.session as session:
            print(ref_url)
            master = session.query(MasterModel).filter_by(referal_link=ref_url).first()
            return master.id

    def subscribe_user_on_master(self, user_id: int, master_id: int):

        with self.session as session:

            existing_subscription = session.query(user_master_association).filter_by(user_id=user_id,
                                                                                     master_id=master_id).first()
            if not existing_subscription:
                print('Subscribed')
                session.execute(user_master_association.insert().values({'user_id': user_id, 'master_id': master_id}))

                session.commit()
            else:
                print('Already in subscribed')
                pass

    def get_user_id_by_telegram_id(self, telegram_id):
        with self.session as session:
            user = session.query(UserModel).filter_by(telegram_id=telegram_id).first()
            session.close()
            if user:
                return user.id

    def subscribe_user_on_master_with_referral_link(self, referral_link, telegram_id):
        master_id = self.get_master_id_by_referral_url(referral_link)
        user_id = self.get_user_id_by_telegram_id(telegram_id)
        self.subscribe_user_on_master(user_id, master_id)

    def get_partners_ids_by_city_id(self, city_id: int) -> list:
        pass

    def get_all_masters_id_by_city_name(self, city_name: str) -> list:
        with self.session as session:
            city = session.query(CityModel).filter_by(name=city_name).first()

            if city:
                masters_ids = []

                for area in city.areas:
                    for master in area.masters:
                        if not master.is_partner:
                            masters_ids.append(master.id)

                return masters_ids
            else:
                return []

    def get_all_partners_id_by_city_name(self, city_name: str) -> list:
        with self.session as session:
            city = session.query(CityModel).filter_by(name=city_name).first()

            if city:
                masters_ids = []

                for area in city.areas:
                    for master in area.masters:
                        if master.is_partner and master:
                            masters_ids.append(master.id)

                return masters_ids
            else:
                return []

    def get_all_masters_ids(self) -> list:
        with self.session as session:
            all_master_ids = session.query(MasterModel.id).filter(MasterModel.is_partner == False).all()
            master_ids = [master_id[0] for master_id in all_master_ids]
            return master_ids

    def get_all_partners_ids(self) -> list:
        with self.session as session:
            all_master_ids = session.query(MasterModel.id).filter(MasterModel.is_partner == True).all()
            master_ids = [master_id[0] for master_id in all_master_ids]
            return master_ids

    def get_city_name_by_area_id(self, city_area_id: int) -> str:
        with self.session as session:
            result = session.query(CityModel.name).join(CityAreaModel).filter(CityAreaModel.id == city_area_id).first()
            city_name = result[0] if result else None
            return city_name

    def get_area_name_by_area_id(self, city_area_id: int) -> str:
        with self.session as session:
            result = session.query(CityAreaModel.name).filter(CityAreaModel.id ==city_area_id).first()
            city_name = result[0] if result else None
            return city_name

    def get_master_id_by_telegram_user_name(self, user_name):
        with self.session as session:
            result = session.query(MasterModel.id).filter(MasterModel.telegram_user_name == user_name).first()
            master_id = result[0] if result else None
            return master_id

    def check_master_visability(self, user_name):
        with self.session as session:
            result = session.query(MasterModel.id).filter(MasterModel.telegram_user_name =='@'+user_name).first()
            if result:
                return True
            else:
                return False


class MailingEngine:
    description: str
    url_to_photo: str | None
    city: str
    district: str | None
    users: list
    db_queries: QueriesToDb

    def __init__(self, queries: QueriesToDb):
        self.db_queries = queries
        self.district = None
        self.url_to_photo = None

    def get_users_from_db_by_district(self) -> None:
        self.users = self.db_queries.all_users_by_district(self.district, self.city)

    def get_users_from_db_by_city(self) -> None:
        self.users = self.db_queries.all_users_by_city(self.city)

    def start_mailing(self, chat_id, bot) -> None:
        if not self.users:
            return bot.send_message(chat_id, 'Нет eще пользователей в выбранной области')

        for i in list(set(self.users)):
            print(f'Отослал сообщение юзеру: {i}')
            if self.url_to_photo is None:
                try:
                    bot.send_message(i, self.description)
                except Exception:
                    pass
            else:
                try:
                    with open(f"beauty_bot/app/photos/{self.url_to_photo}", 'rb') as photo:
                        bot.send_photo(i, photo, caption=self.description)
                except Exception:
                    pass

        return bot.send_message(chat_id, "Рассылка запущена")

    def fill_users(self) -> None:
        if self.district == 'all':
            self.get_users_from_db_by_city()
        else:
            self.get_users_from_db_by_district()


class BaseMenuClass:
    page: int = 0
    content_ids: list

    def up_page(self) -> None:
        if self.page + 1 == len(self.content_ids):
            pass
        else:
            self.page += 1

    def down_page(self) -> None:
        if self.page == 0:
            pass
        else:
            self.page -= 1

    def count_numbers(self) -> str:
        return f'{self.page + 1}/{len(self.content_ids)}'


class MenuWithQuestionnairesEngine(BaseMenuClass):
    telegram_user_id: int
    referral_link: str
    master_data: dict

    def __init__(self, db: QueriesToDb, telegram_user_id):
        self.db = db
        self.telegram_user_id = telegram_user_id
        self.get_user_masters_subscribed_ids()

    def get_data_for_questionary(self) -> None:
        self.master_data = self.db.get_data_for_master_questionary_by_id(self.content_ids[self.page])

    def get_user_masters_subscribed_ids(self) -> None:
        self.content_ids = self.db.get_all_user_signed_masters_id_with_user_by_id(self.telegram_user_id)

    def move_number_to_first(self, master_id) -> None:
        if master_id in self.content_ids:
            self.content_ids.remove(master_id)
            self.content_ids.insert(0, master_id)

    def set_referral_link(self, link):
        self.referral_link = link
        master_id = self.db.get_master_id_by_referral_url(self.referral_link)
        self.move_number_to_first(master_id)

    def up_page(self) -> None:
        if self.page + 1 == len(self.content_ids):
            pass
        else:
            self.page += 1

        self.get_user_masters_subscribed_ids()

    def down_page(self) -> None:
        if self.page == 0:
            pass
        else:
            self.page -= 1
        self.get_user_masters_subscribed_ids()


class MenuWithPartnersQuestionnaires(MenuWithQuestionnairesEngine):
    def __init__(self, db: QueriesToDb, telegram_user_id, city_id):
        super().__init__(db, telegram_user_id)
        self.city_id = city_id
        self.partners_ids_by_area_id()

    def partners_ids_by_area_id(self) -> None:
        self.content_ids = self.db.all_partners_by_area_id(self.city_id)

    def up_page(self) -> None:
        if self.page + 1 == len(self.content_ids):
            pass
        else:
            self.page += 1

        self.partners_ids_by_area_id()

    def down_page(self) -> None:
        if self.page == 0:
            pass
        else:
            self.page -= 1
        self.partners_ids_by_area_id()


class AdminMenuBase(BaseMenuClass):

    def __init__(self, db: QueriesToDb):
        self.db = db

    def create_message_for_questionary(self, data: dict) -> str:
        message = f"{data['description']} \n"
        return message


class AdminMenuMasters(AdminMenuBase):
    master_data: dict
    selected_city_for_masters: str
    city_name: str
    area_name: str

    def __init__(self, db: QueriesToDb):
        super().__init__(db)

    def get_masters_ids_by_city_name(self) -> None:
        self.content_ids = self.db.get_all_masters_id_by_city_name(self.selected_city_for_masters)
        if not self.content_ids:
            raise Exception

    def get_data_for_questionary(self) -> None:
        self.master_data = self.db.get_data_for_master_questionary_by_id(self.content_ids[self.page])
        self.city_name = self.db.get_city_name_by_area_id(self.master_data['location_id'])
        self.area_name = self.db.get_area_name_by_area_id(self.master_data['location_id'])

    def get_description(self) -> str:
        return self.create_message_for_questionary(self.master_data)

    def get_all_masters(self) -> None:
        self.content_ids = self.db.get_all_masters_ids()


class AdminMenuPartners(AdminMenuBase):
    master_data: dict
    selected_city_for_partners: str
    city_name: str
    area_name: str

    def __init__(self, db: QueriesToDb):
        super().__init__(db)

    def get_partners_ids_by_city_name(self):
        self.content_ids = self.db.get_all_partners_id_by_city_name(self.selected_city_for_partners)
        if not self.content_ids:
            raise Exception

    def get_data_for_questionary(self) -> None:
        self.master_data = self.db.get_data_for_master_questionary_by_id(self.content_ids[self.page])
        self.city_name = self.db.get_city_name_by_area_id(self.master_data['location_id'])
        self.area_name = self.db.get_area_name_by_area_id(self.master_data['location_id'])

    def get_description(self) -> str:
        return self.create_message_for_questionary(self.master_data)

    def get_all_partners_ids(self):
        self.content_ids = self.db.get_all_partners_ids()

