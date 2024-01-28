from beauty_bot.app.models import CityModel, CityAreaModel, MasterModel, UserModel


def add_test_data_to_db(session):
    city1 = CityModel(name=f'City1')
    area1 = CityAreaModel(name='Area1', city=city1)
    master1 = MasterModel(
        telegram_user_name=123,
        key='key1',
        referal_link='link1',
        description='Description for master 1',
        username='master1',
        url_to_photo='photo1',
        is_partner=False,
        is_active=True,
        location_id=1,
        reviews_url='reviews1',
        master_portfolio_url='portfolio1'
    )

    city2 = CityModel(name='City2')
    area2 = CityAreaModel(name='Area2', city=city2)
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

    partner1 = MasterModel(
        telegram_user_name=555,
        key='key3',
        referal_link='link3',
        description='Description for partner 1',
        username='partner1',
        url_to_photo='photo3',
        is_partner=True,
        is_active=True,
        location_id=1,
        reviews_url='reviews2',
        master_portfolio_url='portfolio2'
    )

    partner2 = MasterModel(
        telegram_user_name=666,
        key='key4',
        referal_link='link4',
        description='Description for partner 2',
        username='partner2',
        url_to_photo='photo4',
        is_partner=True,
        is_active=True,
        location_id=2,
        reviews_url='reviews2',
        master_portfolio_url='portfolio2'
    )

    user1 = UserModel(telegram_id=789, masters=[master1])
    user2 = UserModel(telegram_id=101, masters=[master2])
    user3 = UserModel(telegram_id=999, masters=[master1])
    user4 = UserModel(telegram_id=1001, masters=[master1, master2])


    # Add data to the session and commit
    session.add_all([city1, area1, master1, city2, area2, master2, user1, user2, user3, partner1, partner2, user4])
    session.commit()

    # Close the session
    session.close()

