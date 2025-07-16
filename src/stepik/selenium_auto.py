from logging import Logger
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

from stepik.exceptions import (
    StepikInvalidPasswordException,
    StepikLoginException,
    StepikRegistrationException,
    StepikUserAlreadyRegisteredException,
)
from users_acquisition import UserData
from selenium.webdriver.remote.webdriver import WebDriver


def register(driver: WebDriver, url: str, user_data: UserData, logger: Logger):
    driver.get(url)
    logger.debug("Trying to register user")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "id_registration_full-name",
                )
            )
        )

    except selenium.common.exceptions.TimeoutException:
        return StepikRegistrationException()
    logger.debug("Found input with id: id_registration_full-name")
    try:
        driver.find_element(By.ID, "id_registration_full-name").send_keys(
            user_data["first_name"] + " " + user_data["last_name"]
        )
        driver.find_element(By.ID, "id_registration_email").send_keys(
            user_data["email"]
        )
        driver.find_element(By.ID, "id_registration_password").send_keys(
            user_data["password"]
        )
        driver.find_element(
            By.XPATH, '//*[@id="registration_form"]/div[2]/div/label'
        ).click()

        driver.find_element(By.XPATH, '//*[@id="registration_form"]/button').click()
    except:
        logger.debug("Error while accessing form inputs")
        raise StepikRegistrationException()
    time.sleep(2)
    if driver.find_elements(By.XPATH, '//*[@id="registration_form"]/button'):
        logger.debug("User already exists")
        raise StepikUserAlreadyRegisteredException()

    # def register(
    #     Fio: str = None, Mail: str = None, Password: str = None, *args, **kwargs
    # ) -> bool:
    #     DRIVER.get(REGISTRATION_URL)
    #     print("Trying to register user")
    #     try:
    #         WebDriverWait(DRIVER, 10).until(
    #             EC.presence_of_element_located(
    #                 (
    #                     By.ID,
    #                     "id_registration_full-name",
    #                 )
    #             )
    #         )

    #     except selenium.common.exceptions.TimeoutException:
    #         return False
    #     print("Found input with id: id_registration_full-name")
    #     try:
    #         DRIVER.find_element(By.ID, "id_registration_full-name").send_keys(Fio)
    #         DRIVER.find_element(By.ID, "id_registration_email").send_keys(Mail)
    #         DRIVER.find_element(By.ID, "id_registration_password").send_keys(Password)
    #         DRIVER.find_element(By.XPATH, '//*[@id="registration_form"]/button').click()
    #     except:
    #         print("Error while accessing form inputs")
    #         return False
    #     time.sleep(2)
    #     if DRIVER.find_elements(By.XPATH, '//*[@id="registration_form"]/button'):
    #         print("User already registered")
    #         return False
    #     print("Successfully Registered user")
    #     return True

    # def login(Mail: str = None, Password: str = None, *args, **kwargs):
    #     DRIVER.get(LOGIN_URL)

    #     try:
    #         WebDriverWait(DRIVER, 10).until(
    #             EC.presence_of_element_located(
    #                 (
    #                     By.ID,
    #                     "id_login_email",
    #                 )
    #             )
    #         )
    #     except selenium.common.exceptions.TimeoutException:
    #         return False
    #     try:
    #         DRIVER.find_element(By.ID, "id_login_email").send_keys(Mail)
    #         DRIVER.find_element(By.ID, "id_login_password").send_keys(Password)
    #         DRIVER.find_element(By.XPATH, '//*[@id="login_form"]/button').click()
    #     except:
    #         return False
    #     time.sleep(2)
    #     if DRIVER.find_elements(By.XPATH, '//*[@id="login_form"]/button'):
    #         return False
    #     return True

    # def enroll(course_ids: list[str]) -> list[bool]:
    # enrolled_courses = list()

    # for course_id in course_ids:
    #     text = (
    #         "Зарегистрировано: "
    #         + str(ENROLLED)
    #         + " людей"
    #         + " | Регистрирует "
    #         + CURRENT_PERSON
    #         + " на "
    #         + str(course_id)
    #     )
    #     print("\r" + text + "                     ", end="")
    #     DRIVER.get(f"https://stepik.org/course/{course_id}/promo")
    #     try:
    #         WebDriverWait(DRIVER, 1).until(
    #             EC.presence_of_element_located(
    #                 (
    #                     By.CSS_SELECTOR,
    #                     "button.course-promo-enrollment__join-btn",
    #                 )
    #             )
    #         )
    #     except selenium.common.exceptions.TimeoutException:
    #         enrolled_courses.append(True)
    #         continue
    #     elements = DRIVER.find_elements(
    #         By.CSS_SELECTOR, "button.course-promo-enrollment__join-btn"
    #     )
    #     if elements:
    #         try:
    #             elements[-1].click()
    #         except:
    #             enrolled_courses.append(False)
    #     time.sleep(0.5)
    #     enrolled_courses.append(True)

    # return enrolled_courses


def login(driver: WebDriver, url: str, user_data: UserData, logger: Logger):
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.ID,
                    "id_login_email",
                )
            )
        )
    except selenium.common.exceptions.TimeoutException:
        raise StepikLoginException()
    try:
        driver.find_element(By.ID, "id_login_email").send_keys(user_data["email"])
        driver.find_element(By.ID, "id_login_password").send_keys(user_data["password"])
        driver.find_element(By.XPATH, '//*[@id="login_form"]/button').click()
    except:
        return StepikLoginException()
    time.sleep(2)
    if driver.find_elements(By.XPATH, '//*[@id="login_form"]/button'):
        return StepikInvalidPasswordException()


def enroll(
    driver: WebDriver,
    base_url: str,
    course_ids: list[str],
    logger: Logger,
):
    enrolled_courses = 0

    for course_id in course_ids:
        url = base_url + course_id
        logger.debug(f"Trying to enroll to {course_id}")
        driver.get(f"{url}/promo")
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "button.course-promo-enrollment__join-btn",
                    )
                )
            )
        except selenium.common.exceptions.TimeoutException:
            enrolled_courses += 1
            continue
        elements = driver.find_elements(
            By.CSS_SELECTOR, "button.course-promo-enrollment__join-btn"
        )
        if elements:
            try:
                elements[-1].click()
            except:
                ...
        time.sleep(0.5)
        enrolled_courses += 1

    return enrolled_courses
