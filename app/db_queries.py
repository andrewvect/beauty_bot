from sqlalchemy import select, and_
from sqlalchemy.orm import sessionmaker

from models import engine, CityModel, CityAreaModel, MasterModel, UserModel, user_master_association

Session = sessionmaker(bind=engine)


def get_area_name_by_id(area_id):
    session = Session()
    area = session.query(CityAreaModel).filter_by(id=area_id).first()
    session.close()
    return area.name


def add_new_city(name):
    session = Session()
    new_city = CityModel(name=name)
    session.add(new_city)
    session.commit()
    session.close()


def add_new_area(city_id, area_name):
    session = Session()
    new_area = CityAreaModel(name=area_name, city_id=city_id)
    session.add(new_area)
    session.commit()
    session.close()


def get_city_id_by_name(city_name):
    session = Session()
    city = session.query(CityModel).filter_by(name=city_name).first()
    session.close()
    return city.id


def get_area_id_by_name(area_name):
    session = Session()
    area = session.query(CityAreaModel).filter_by(name=area_name).first()
    session.close()
    return area.id


def get_all_cities():
    session = Session()
    city_names = session.query(CityModel.name).all()
    session.close()
    return [name[0] for name in city_names]


def get_all_areas_by_city_name(city_name):
    session = Session()
    areas = (
        session.query(CityAreaModel.name)
            .join(CityModel)
            .filter(CityModel.name == city_name)
            .all()
    )
    session.close()
    return [area[0] for area in areas]


def get_city_name_by_area_id(area_id):
    session = Session()
    city_area = session.query(CityAreaModel).filter_by(id=area_id).first()
    city_name = city_area.city.name
    session.close()
    return city_name


def get_user_telegram_id_by_id(id):
    session = Session()
    user = session.query(UserModel).filter_by(id=id).first()
    user_telegram_id = user.telegram_id
    session.close()
    return user_telegram_id


def add_new_master(telegram_usermane, key, referal_link, description, username, url_to_photo, is_partner, is_active,
                   location_id, reviews_url, master_portfolio_url):
    session = Session()

    master = MasterModel(telegram_user_name=telegram_usermane,
                         key=key,
                         referal_link=referal_link,
                         description=description,
                         username=username,
                         url_to_photo=url_to_photo,
                         is_partner=is_partner,
                         is_active=is_active,
                         location_id=location_id,
                         reviews_url=reviews_url,
                         master_portfolio_url=master_portfolio_url)

    session.add(master)
    session.commit()
    session.close()


def get_questionares_by_type(type):
    session = Session()
    questionaries = session.query(MasterModel.id,
                                  MasterModel.description,
                                  MasterModel.is_active,
                                  MasterModel.url_to_photo,
                                  MasterModel.location_id).filter_by(is_partner=type).all()
    session.close()
    data = []

    for id, description, is_active, url_to_photo, area_id in questionaries:
        area_name = get_area_name_by_id(area_id)
        city_name = get_city_name_by_area_id(area_id)

        data.append({'description': description,
                     'is_active': is_active,
                     'url_to_photo': url_to_photo,
                     'city_name': city_name,
                     'area_name': area_name,
                     'master_id': id})

    return data


def get_masters_partners_by_ids(master_ids, is_partner=None):
    session = Session()
    query = session.query(MasterModel).filter(MasterModel.id.in_(master_ids))

    if is_partner is not None:
        query = query.filter(MasterModel.is_partner == is_partner)

    masters = query.all()
    session.close()

    data = []

    for master in masters:
        area_name = get_area_name_by_id(master.location_id)
        city_name = get_city_name_by_area_id(master.location_id)

        data.append({'description': master.description,
                     'is_active': master.is_active,
                     'url_to_photo': master.url_to_photo,
                     'city_name': city_name,
                     'area_name': area_name,
                     'master_id': master.id})

    return data


def get_masters_questionaries_for_admin_menu_by_city(page, masters_ids):
    questionary = get_masters_partners_by_ids(masters_ids, is_partner=False)
    count_of_questionaries = len(questionary)
    return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}


def get_partners_questionaries_for_admin_menu_by_city(page, masters_ids):
    questionary = get_masters_partners_by_ids(masters_ids, is_partner=True)
    count_of_questionaries = len(questionary)
    return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}


def get_masters_questionaries_for_admin_menu(page):
    questionary = get_questionares_by_type(False)
    count_of_questionaries = len(questionary)
    return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}


def get_partners_questionaries_for_admin_menu(page):
    questionary = get_questionares_by_type(True)
    count_of_questionaries = len(questionary)
    return {'questionary': questionary[page - 1], 'page_counter': count_of_questionaries}


def get_all_master_subscribers_by_master_telegram_username(telegram_username):
    session = Session()
    master = session.query(MasterModel).filter_by(telegram_user_name='@' + telegram_username).first()

    # Получаем всех подписчиков мастера
    query = select([user_master_association.c.user_id]).where(user_master_association.c.master_id == master.id)
    result = session.execute(query)
    subscribers_id = [row[0] for row in result.fetchall()]

    subscribers_telegram_id = []
    for id in subscribers_id:
        subscribers_telegram_id.append(get_user_telegram_id_by_id(id))

    session.close()

    return subscribers_telegram_id


def get_key_by_telegram_username(telegram_user_name):
    session = Session()
    master = session.query(MasterModel).filter_by(telegram_user_name=telegram_user_name).first()

    if master:
        key = master.key
    else:
        key = None

    session.close()
    return key


def get_master_id_by_ref_url(ref_url):
    session = Session()
    master = session.query(MasterModel).filter_by(referal_link=ref_url).first()
    session.close()
    if master:
        return master.id
    return None


def check_if_user_in_db(user_id):
    session = Session()
    user = session.query(UserModel).filter_by(telegram_id=user_id).first()
    session.close()
    if user:
        return True
    return False


def add_new_user_to_db(user_id):
    session = Session()
    new_city = UserModel(telegram_id=user_id)
    session.add(new_city)
    session.commit()
    session.close()


def get_user_id_by_telegram_id(telegram_id):
    session = Session()
    master = session.query(UserModel).filter_by(telegram_id=telegram_id).first()
    session.close()
    if master:
        return master.id
    return None


def subscribe_user_on_master(user_id, ref_url):
    if check_if_user_in_db(user_id) is False:
        add_new_user_to_db(user_id)

    session = Session()

    master_id = get_master_id_by_ref_url(ref_url)
    user_id = get_user_id_by_telegram_id(user_id)

    existing_subscription = session.query(user_master_association).filter_by(user_id=user_id, master_id=master_id).first()
    if not existing_subscription:
        session.execute(user_master_association.insert().values({'user_id': user_id, 'master_id': master_id}))

        session.commit()

        session.close()
    else:
        session.close()
        print('Already in subscribed')
        pass


def get_master_photo_name_by_telegram_username(master_telegram_user_name):
    session = Session()

    master = session.query(MasterModel).filter_by(telegram_user_name=master_telegram_user_name).first()
    session.close()

    return master.url_to_photo


def get_all_user_subscribe_profiles(user_telegram_id):
    session = Session()
    user = session.query(UserModel).filter_by(telegram_id=user_telegram_id).first()

    if user:
        masters_ids = [master.id for master in user.masters]
        session.close()
        return masters_ids
    else:
        session.close()
        print("Пользователь с указанным telegram_id не найден")


def get_all_partner_subscribe_profiles(user_telegram_id):
    session = Session()
    master_ids = get_all_user_subscribe_profiles(user_telegram_id)
    partners_ids = [
        master_id for master_id in master_ids if
        session.query(MasterModel.is_partner)
            .filter_by(id=master_id, is_active=True)  # Добавляем фильтрацию по is_active
            .scalar()
    ]
    session.close()
    return partners_ids


def get_all_master_subscribe_profiles(user_telegram_id):
    session = Session()
    master_ids = get_all_user_subscribe_profiles(user_telegram_id)
    filtered_master_ids = [
        master_id for master_id in master_ids if
        session.query(MasterModel)
            .filter_by(id=master_id, is_active=True, is_partner=False)
            .all()
    ]
    session.close()
    return filtered_master_ids


def get_questionary_for_user_menu_by_id(master_id):
    session = Session()
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

    session.close()

    area_name = get_area_name_by_id(questionary.location_id)
    city_name = get_city_name_by_area_id(questionary.location_id)

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


def get_masters_profiles_for_user_menu(master_id):
    return get_questionary_for_user_menu_by_id(master_id)


def get_partner_profiles_for_user_menu(partner_id):
    return get_questionary_for_user_menu_by_id(partner_id)


def get_master_telegram_url_by_id(master_id):
    session = Session()
    master = session.query(MasterModel).filter_by(id=master_id).first()
    session.close()
    if master:
        return master.telegram_user_name
    return None


def get_master_portfolio_url_by_id(master_id):
    session = Session()
    master = session.query(MasterModel).filter_by(id=master_id).first()
    session.close()
    if master:
        return master.master_portfolio_url
    return None


def get_master_reviews_url_by_id(master_id):
    session = Session()
    master = session.query(MasterModel).filter_by(id=master_id).first()
    session.close()
    if master:
        return master.reviews_url
    return None


def set_master_active_profile(master_id):
    print(master_id)
    session = Session()
    master = session.query(MasterModel).filter_by(id=master_id).first()
    master.is_active = not master.is_active
    session.commit()
    session.close()


def get_all_masters_id_by_name_city(city_name):
    try:
        session = Session()

        city = session.query(CityModel).filter_by(name=city_name).first()

        if city:
            masters_ids = []

            for area in city.areas:
                for master in area.masters:
                    if not master.is_partner:
                        masters_ids.append(master.id)

            session.close()
            return masters_ids
    except Exception:
        return []


def get_all_partners_id_by_name_city(city_name):
    try:
        session = Session()

        city = session.query(CityModel).filter_by(name=city_name).first()

        if city:
            partners_ids = []

            for area in city.areas:
                for master in area.masters:
                    if master.is_partner:
                        partners_ids.append(master.id)

            session.close()
            return partners_ids
    except Exception:
        return []