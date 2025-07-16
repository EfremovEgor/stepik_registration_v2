from abc import ABC, abstractmethod
from typing import TypedDict
from helpers import generate_random_email, generate_random_password
from mimesis import Person
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Locale


class UserData(TypedDict):
    first_name: str | None
    last_name: str | None
    phone: str | None
    email: str
    password: str


class BaseUserAcquisition(ABC):
    @abstractmethod
    def get_users(self, amount: int) -> list[UserData]: ...


class RandomUserAcquisition(BaseUserAcquisition):

    def get_users(self, amount: int) -> list[UserData]:
        users: list[UserData] = []
        for _ in range(amount):
            person = Person(Locale.RU)
            users.append(
                {
                    "email": generate_random_email(),
                    "password": generate_random_password(),
                    "first_name": person.name(),
                    "last_name": person.last_name(),
                    "phone": person.telephone(mask="+7##########"),
                }
            )
        return users
