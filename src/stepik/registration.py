import logging


from base_course_registration import BaseCourseRegistration
from registration_patterns import BaseRegistrationPattern
from helpers import try_sleep
from driver import get_driver
from .selenium_auto import enroll, login, register
from .exceptions import (
    StepikRegistrationException,
    StepikEnrollmentException,
    StepikInvalidPasswordException,
    StepikLoginException,
    StepikUserAlreadyRegisteredException,
)
from users_acquisition import BaseUserAcquisition, UserData
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium
import csv
import time
import sys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver


class StepikCourseRegistration(BaseCourseRegistration):
    base_url = "https://stepik.org"
    registration_url = base_url + "/registration"
    login_url = base_url + "/login"
    base_course_url = base_url + "/course/"

    def __init__(self, logger):
        super().__init__(logger)

    def run(
        self,
        strategy: BaseUserAcquisition,
        registration_pattern: BaseRegistrationPattern,
        courses: list[str],
    ):

        self.log(
            logging.INFO,
            f"Всего необходимо зарегистрировать {registration_pattern.get_total_to_register()} пользователей",
        )

        users = strategy.get_users(registration_pattern.get_total_to_register())
        self.log(
            logging.INFO,
            f"Получено {len(users)} пользователей",
        )

        current_position = 0
        batch_number = 0
        while self.total_registered < registration_pattern.total_to_register:
            batch_size = registration_pattern.get_next_batch_size()
            current_bias = 0
            total_registered_in_this_batch = 0
            self.log(
                logging.INFO,
                f"Начинаю работу с {batch_number+1} пакетом состоящим из {batch_size} пользователей",
            )

            while total_registered_in_this_batch < batch_size:
                i = current_bias + current_position
                if i >= len(users):
                    self.log(
                        logging.WARNING,
                        f"Пользователи закончились, получилось зарегистрировать {self.total_registered} из {registration_pattern.total_to_register} пользователей",
                    )
                    self._exit()
                    return
                user = users[i]
                self.log(
                    logging.INFO,
                    f"Начинаю работу с {i+1} пользователем: {user}",
                )
                driver = get_driver()
                try:
                    self._try_register_account(driver, user)
                    self.log(
                        logging.INFO,
                        f"Получилось зарегистрироваться",
                    )
                except StepikRegistrationException:
                    self.log(
                        logging.WARNING,
                        f"Не получилось зарегистрировать  {i+1} пользователя, перехожу к другому",
                    )
                    current_bias += 1
                    continue
                except StepikUserAlreadyRegisteredException:
                    self.log(
                        logging.WARNING,
                        f"Пользователь {i+1} пользователя уже зарегистрирован, пытаюсь войти",
                    )
                    if not self._try_login_into_account(driver, user):

                        self.log(
                            logging.ERROR,
                            f"Данные от аккаунта {i+1} пользователя неверны, перехожу к другому",
                        )

                        current_bias += 1
                        continue

                    # self.log(
                    #     logging.INFO,
                    #     f"Начинаю регистрацию {i+1} пользователя на курс {course}",
                    # )
                self.log(
                    logging.INFO,
                    f"Начинаю регистрацию {i+1} пользователя на {" ".join(courses)}",
                )
                amount = self._try_enroll_to_course(driver, courses)
                driver.quit()

                total_registered_in_this_batch += 1
                current_bias += 1
                self.total_registered += amount

                self.log(
                    logging.INFO,
                    f"Пользователя {i+1} получилось зарегистрировать на {amount} курсов",
                )
                self.log(
                    logging.INFO,
                    f"Зарегистрировано всего {self.total_registered} из {registration_pattern.total_to_register} в сумме по всем курсам",
                )

                sleep_time = registration_pattern.get_next_interval()

                if sleep_time is not None:
                    self.log(
                        logging.INFO,
                        f"Приостанавливаю выполнение программы на {sleep_time} секунд между пользователями",
                    )
                try_sleep(sleep_time)
            current_position += current_bias
            batch_number += 1

            sleep_time = registration_pattern.get_next_interval_between_batches()
            if sleep_time is not None:
                self.log(
                    logging.INFO,
                    f"Приостанавливаю выполнение программы на {sleep_time} секунд между пакетами",
                )
            try_sleep(sleep_time)
        self._exit()

    def get_base_url(self):
        return self.base_url

    def _try_register_account(
        self, driver: WebDriver, user: UserData, max_attempts: int = 5
    ):
        attempts = 0
        for _ in range(max_attempts):
            try:
                register(driver, self.registration_url, user, self.logger)
                return True
            except StepikRegistrationException:
                attempts += 1
                continue
            except StepikUserAlreadyRegisteredException:
                raise StepikUserAlreadyRegisteredException()
        raise StepikRegistrationException()

    def _try_login_into_account(
        self, driver: WebDriver, user: UserData, max_attempts: int = 5
    ):
        attempts = 0
        for _ in range(max_attempts):
            try:
                login(driver, self.registration_url, user, self.logger)
                return True
            except StepikLoginException:
                attempts += 1
                continue
            except StepikInvalidPasswordException:
                return False
        return False

    def _try_enroll_to_course(self, driver: WebDriver, course_ids: list[str]):
        return enroll(driver, self.base_course_url, course_ids, self.logger)

    def _exit(self):
        self.log(
            logging.INFO,
            f"Программа завершила выполнение, зарегистрировано {self.total_registered} пользователей",
        )
