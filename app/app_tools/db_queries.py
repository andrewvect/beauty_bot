from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from models import engine, CityModel, CityAreaModel, MasterModel, UserModel, user_master_association


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
            result = session.query(CityAreaModel.name).filter(CityAreaModel.id == city_area_id).first()
            city_name = result[0] if result else None
            return city_name

    def get_master_id_by_telegram_user_name(self, user_name):
        with self.session as session:
            result = session.query(MasterModel.id).filter(MasterModel.telegram_user_name == user_name).first()
            master_id = result[0] if result else None
            return master_id

    def check_master_visability(self, user_name):
        with self.session as session:
            result = session.query(MasterModel.id).filter(MasterModel.telegram_user_name == '@' + user_name).first()
            if result:
                return True
            else:
                return False

    def get_area_name_by_id(self, area_id: int) -> str:
        with self.session as session:
            area = session.query(CityAreaModel).filter_by(id=area_id).first()
            return area.name

    def add_new_city(self, name):
        with self.session as session:
            name = name.lower()
            new_city = CityModel(name=name)
            session.add(new_city)
            session.commit()

    def check_if_city_exist(self, name):
        with self.session as session:
            name = name.lower()
            city = session.query(CityModel).filter_by(name=name).first()

            if city:
                return True
            else:
                return False

    def check_if_area_exist(self, name, city_id):
        with self.session as session:
            name = name.lower()
            area = session.query(CityAreaModel).filter_by(name=name, city_id=city_id).first()

            if area:
                return True
            else:
                return False

    def add_new_area(self, city_id, area_name):
        with self.session as session:
            area_name = area_name.lower()
            new_area = CityAreaModel(name=area_name, city_id=city_id)
            session.add(new_area)
            session.commit()

    def get_city_id_by_name(self, city_name):
        with self.session as session:
            city = session.query(CityModel).filter_by(name=city_name).first()
            return city.id

    def get_area_id_by_name(self, area_name):
        with self.session as session:
            area = session.query(CityAreaModel).filter_by(name=area_name).first()
            return area.id

    def get_all_cities(self):
        with self.session as session:
            city_names = session.query(CityModel.name).all()
            return [name[0] for name in city_names]

    def get_all_areas_by_city_name(self, city_name):
        with self.session as session:
            areas = (
                session.query(CityAreaModel.name)
                    .join(CityModel)
                    .filter(CityModel.name == city_name)
                    .all()
            )
            return [area[0] for area in areas]

    def get_user_telegram_id_by_id(self, id):
        with self.session as session:
            user = session.query(UserModel).filter_by(id=id).first()
            user_telegram_id = user.telegram_id
            return user_telegram_id

    def add_new_master(self, new_master_state, key, referal_link, is_active,
                       location_id):
        with self.session as session:
            master = MasterModel(telegram_user_name=new_master_state['telegram_username'],
                                 key=key,
                                 referal_link=referal_link,
                                 description=new_master_state['description'],
                                 username=new_master_state['username'],
                                 url_to_photo=new_master_state['file_name'],
                                 is_partner=new_master_state['is_partner'],
                                 is_active=is_active,
                                 location_id=location_id,
                                 reviews_url=new_master_state['reviews_url'],
                                 master_portfolio_url=new_master_state['portfolio_url'])

            session.add(master)
            session.commit()

    def get_questionares_by_type(self, type):
        with self.session as session:
            questionaries = session.query(MasterModel.id,
                                          MasterModel.description,
                                          MasterModel.is_active,
                                          MasterModel.url_to_photo,
                                          MasterModel.location_id).filter_by(is_partner=type).all()
            data = []

            for id, description, is_active, url_to_photo, area_id in questionaries:
                area_name = self.get_area_name_by_id(area_id)
                city_name = self.get_city_name_by_area_id(area_id)

                data.append({'description': description,
                             'is_active': is_active,
                             'url_to_photo': url_to_photo,
                             'city_name': city_name,
                             'area_name': area_name,
                             'master_id': id})

            return data

    def get_masters_partners_by_ids(self, master_ids, is_partner=None):
        with self.session as session:
            query = session.query(MasterModel).filter(MasterModel.id.in_(master_ids))

            if is_partner is not None:
                query = query.filter(MasterModel.is_partner == is_partner)

            masters = query.all()

            data = []

            for master in masters:
                area_name = self.get_area_name_by_id(master.location_id)
                city_name = self.get_city_name_by_area_id(master.location_id)

                data.append({'description': master.description,
                             'is_active': master.is_active,
                             'url_to_photo': master.url_to_photo,
                             'city_name': city_name,
                             'area_name': area_name,
                             'master_id': master.id})

            return data

    def get_masters_questionaries_for_admin_menu_by_city(self, page, masters_ids):
        questionary = self.get_masters_partners_by_ids(masters_ids, is_partner=False)
        count_of_questionaries = len(questionary)
        return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}

    def get_partners_questionaries_for_admin_menu_by_city(self, page, masters_ids):
        questionary = self.get_masters_partners_by_ids(masters_ids, is_partner=True)
        count_of_questionaries = len(questionary)
        return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}

    def get_masters_questionaries_for_admin_menu(self, page):
        questionary = self.get_questionares_by_type(False)
        count_of_questionaries = len(questionary)
        return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}

    def get_partners_questionaries_for_admin_menu(self, page):
        questionary = self.get_questionares_by_type(True)
        count_of_questionaries = len(questionary)
        return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}

    def get_all_master_subscribers_by_master_telegram_username(self, telegram_username):
        with self.session as session:
            master = session.query(MasterModel).filter_by(telegram_user_name='@' + telegram_username).first()

            # Получаем всех подписчиков мастера
            query = select([user_master_association.c.user_id]).where(user_master_association.c.master_id == master.id)
            result = session.execute(query)
            subscribers_id = [row[0] for row in result.fetchall()]

            subscribers_telegram_id = []
            for id in subscribers_id:
                subscribers_telegram_id.append(self.get_user_telegram_id_by_id(id))

            return subscribers_telegram_id

    def get_key_by_telegram_username(self, telegram_user_name):
        with self.session as session:
            master = session.query(MasterModel).filter_by(telegram_user_name=telegram_user_name).first()

            if master:
                key = master.key
            else:
                key = None

            return key

    def get_master_id_by_ref_url(self, ref_url):
        with self.session as session:
            master = session.query(MasterModel).filter_by(referal_link=ref_url).first()
            if master:
                return master.id
            return None

    def check_if_user_in_db(self, user_id):
        with self.session as session:
            user = session.query(UserModel).filter_by(telegram_id=user_id).first()
            if user:
                return True
            return False

    def add_new_user_to_db(self, user_id):
        with self.session as session:
            new_city = UserModel(telegram_id=user_id)
            session.add(new_city)
            session.commit()

    def subscribe_user_on_master2(self, user_id, ref_url):
        with self.session as session:
            if self.check_if_user_in_db(user_id) is False:
                self.add_new_user_to_db(user_id)

            master_id = self.get_master_id_by_ref_url(ref_url)
            user_id = self.get_user_id_by_telegram_id(user_id)

            existing_subscription = session.query(user_master_association).filter_by(user_id=user_id,
                                                                                     master_id=master_id).first()
            if not existing_subscription:
                session.execute(user_master_association.insert().values({'user_id': user_id, 'master_id': master_id}))
                session.commit()
            else:
                print('Already in subscribed')
                pass

    def get_master_photo_name_by_telegram_username(self, master_telegram_user_name):
        with self.session as session:
            master = session.query(MasterModel).filter_by(telegram_user_name=master_telegram_user_name).first()

            return master.url_to_photo

    def get_all_user_subscribe_profiles(self, user_telegram_id):
        with self.session as session:
            user = session.query(UserModel).filter_by(telegram_id=user_telegram_id).first()

            masters_ids = [master.id for master in user.masters]
            return masters_ids

    def get_all_partner_subscribe_profiles(self, user_telegram_id):
        with self.session as session:
            master_ids = self.get_all_user_subscribe_profiles(user_telegram_id)
            partners_ids = [
                master_id for master_id in master_ids if
                session.query(MasterModel).filter_by(id=master_id, is_active=True, is_partner=True).scalar()
            ]
            return partners_ids

    def get_all_master_subscribe_profiles(self, user_telegram_id):
        with self.session as session:
            master_ids = self.get_all_user_subscribe_profiles(user_telegram_id)

            master_ids = [
                master_id for master_id in master_ids if
                session.query(MasterModel).filter_by(id=master_id, is_active=True, is_partner=False).scalar()
            ]

            return master_ids

    def get_questionary_for_user_menu_by_id(self, master_id):
        with self.session as session:
            questionary = session.query(
                MasterModel.id,
                MasterModel.url_to_photo,
                MasterModel.username,
                MasterModel.location_id,
                MasterModel.description,
                MasterModel.telegram_user_name,
                MasterModel.is_active,
                MasterModel.reviews_url,
                MasterModel.master_portfolio_url
            ).filter(MasterModel.id == master_id).first()

            area_name = self.get_area_name_by_id(questionary.location_id)
            city_name = self.get_city_name_by_area_id(questionary.location_id)

            questionary_dict = {
                'id': questionary.id,
                'url_to_photo': questionary.url_to_photo,
                'username': questionary.username,
                'location_id': questionary.location_id,
                'description': questionary.description,
                'telegram_user_name': questionary.telegram_user_name,
                'reviews_url': questionary.reviews_url,
                'master_portfolio_url': questionary.master_portfolio_url,
                'area': area_name,
                'city': city_name
            }

            return questionary_dict

    def get_masters_profiles_for_user_menu(self, master_id):
        return self.get_questionary_for_user_menu_by_id(master_id)

    def get_partner_profiles_for_user_menu(self, partner_id):
        return self.get_questionary_for_user_menu_by_id(partner_id)

    def get_master_telegram_url_by_id(self, master_id):
        with self.session as session:
            master = session.query(MasterModel).filter_by(id=master_id).first()
            if master:
                return master.telegram_user_name
            return None

    def get_master_portfolio_url_by_id(self, master_id):
        with self.session as session:
            master = session.query(MasterModel).filter_by(id=master_id).first()
            if master:
                return master.master_portfolio_url
            return None

    def get_master_reviews_url_by_id(self, master_id):
        with self.session as session:
            master = session.query(MasterModel).filter_by(id=master_id).first()
            if master:
                return master.reviews_url
            return None

    def set_master_active_profile(self, master_id):
        with self.session as session:
            master = session.query(MasterModel).filter_by(id=master_id).first()
            master.is_active = not master.is_active
            session.commit()

    def get_all_masters_id_by_name_city(self, city_name):
        with self.session as session:
            try:

                city = session.query(CityModel).filter_by(name=city_name).first()

                if city:
                    masters_ids = []

                    for area in city.areas:
                        for master in area.masters:
                            if not master.is_partner:
                                masters_ids.append(master.id)

                    return masters_ids
            except Exception:
                return []

    def get_all_partners_id_by_name_city(self, city_name):
        with self.session as session:
            try:

                city = session.query(CityModel).filter_by(name=city_name).first()
                if city:
                    partners_ids = []

                    for area in city.areas:
                        for master in area.masters:
                            if master.is_partner:
                                partners_ids.append(master.id)

                    return partners_ids
            except Exception:
                return []

    def add_user_to_database(self, telegram_id):
        with self.session as session:
            existing_user = session.query(UserModel).filter_by(telegram_id=telegram_id).first()

            if existing_user:
                print(f"Пользователь с telegram_id {telegram_id} уже существует в базе данных.")
                return

            new_user = UserModel(telegram_id=telegram_id)

            session.add(new_user)

            session.commit()


Session = sessionmaker(bind=engine)
db = QueriesToDb(Session)