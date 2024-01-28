import os
import unittest

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from beauty_bot.app.models import Base as bs

from .fixtures import add_test_data_to_db


class Base(unittest.TestCase):
    def setUp(self) -> None:
        test_engine = create_engine("sqlite:///test.beauty_bot.db")
        bs.metadata.create_all(test_engine)
        self.Session = sessionmaker(bind=test_engine)
        self.fill_db_test_data()

    def tearDown(self) -> None:
        path_to_db = 'test.beauty_bot.db'
        try:
            os.remove(path_to_db)
            print(f'Файл {path_to_db} успешно удален.')
        except OSError as e:
            print(f'Ошибка при удалении файла {path_to_db}: {e}')

    def fill_db_test_data(self):
        add_test_data_to_db(self.Session())

