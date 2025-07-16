from enum import Enum
import random
import string
from time import sleep


class EmailProvider(str, Enum):
    gmail = "gmail.com"
    yandex = "yandex.ru"
    mail = "mail.ru"
    rambler = "rambler.ru"
    yahoo = "yahoo.com"


def get_random_email_provider() -> EmailProvider:
    return random.choice(list(EmailProvider))


def generate_random_email(domain: str | None = None, length: int = 10):
    if domain == None:
        domain = get_random_email_provider().value
    characters = string.ascii_lowercase + string.digits
    username = "".join(random.choice(characters) for _ in range(length))
    email = f"{username}@{domain}"
    return email


def generate_random_password(length: int = 12):
    characters = string.ascii_lowercase + string.digits
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def try_sleep(time: int | None):
    if time is not None:
        sleep(time)
