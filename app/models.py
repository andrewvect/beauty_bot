from sqlalchemy import create_engine


from sqlalchemy import Table, Column, Integer, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

user_master_association = Table('user_master_association', Base.metadata,
                                Column('user_id', Integer, ForeignKey('users.id')),
                                Column('master_id', Integer, ForeignKey('masters.id'))
                                )


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)

    masters = relationship('MasterModel', secondary=user_master_association, back_populates='users')


class MasterModel(Base):
    __tablename__ = 'masters'

    id = Column(Integer, primary_key=True)
    telegram_user_name = Column(BigInteger, unique=True)
    key = Column(String(50), unique=True, nullable=False)
    referal_link = Column(String(100), unique=True, nullable=False)
    description = Column(String(500))
    username = Column(String(100), unique=False, nullable=False)
    url_to_photo = Column(String(200), unique=True, nullable=False)
    is_partner = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    location_id = Column(Integer, ForeignKey('areas.id'))
    reviews_url = Column(String(200), nullable=False)
    master_portfolio_url = Column(String(200), nullable=False)

    users = relationship('UserModel', secondary=user_master_association, back_populates='masters')
    areas = relationship('CityAreaModel', back_populates='masters')  # Изменено 'areas' на 'masters'.


class CityModel(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    areas = relationship('CityAreaModel', back_populates='city')


class CityAreaModel(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=False, nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'))

    masters = relationship('MasterModel', back_populates='areas')
    city = relationship('CityModel', back_populates='areas')

    def __str__(self):
        return self.name


engine = create_engine("sqlite:///beauty_bot.db")

