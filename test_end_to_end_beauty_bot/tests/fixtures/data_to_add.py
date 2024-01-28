from beauty_bot.app.models import CityModel, CityAreaModel, MasterModel, UserModel


def add_test_data_to_db(session):
    city1 = CityModel(name=f'city1')
    area1 = CityAreaModel(name='area1', city=city1)
    master1 = MasterModel(
        telegram_user_name='@lil_loadedsd',
        key='key1',
        referal_link='link1',
        description='Description for master 1',
        username='master1',
        url_to_photo='photo1',
        is_partner=True,
        is_active=True,
        location_id=1,
        reviews_url='reviews1',
        master_portfolio_url='portfolio1'
    )

    city2 = CityModel(name='city2')
    area2 = CityAreaModel(name='area2', city=city2)
    master2 = MasterModel(
        telegram_user_name=456,
        key='key2',
        referal_link='link2',
        description='Description for master 2',
        username='master2',
        url_to_photo='photo2',
        is_partner=False,
        is_active=True,
        location_id=2,
        reviews_url='reviews2',
        master_portfolio_url='portfolio2'
    )

    user1 = UserModel(telegram_id=789, masters=[master1])
    user2 = UserModel(telegram_id=101, masters=[master2])
    user3 = UserModel(telegram_id=999, masters=[master1])

    # Add data to the session and commit
    session.add_all([city1, area1, master1, city2, area2, master2, user1, user2, user3])
    session.commit()

    # Close the session
    session.close()

