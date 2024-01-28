import string
import random

from sqlalchemy.orm import sessionmaker

from models import engine
from beauty_bot.app.tools import QueriesToDb

import secrets

selected_area = ''
Session = sessionmaker(bind=engine)

queries_to_db = QueriesToDb(Session)


def generate_10_digit_key():
    key = ''.join(secrets.choice('0123456789') for _ in range(10))
    return key


def generate_key(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string


def is_login_command(message):
    split_str = message.text.lower().split()
    if split_str[0] == '/login' and len(split_str) == 2:
        return True
    else:
        return False