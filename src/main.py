from abc import ABC, abstractmethod
import logging
import random
from typing import Callable, TypedDict
from registration_patterns import BaseRegistrationPattern
from base_course_registration import BaseCourseRegistration
from stepik.registration import StepikCourseRegistration
from users_acquisition import BaseUserAcquisition, RandomUserAcquisition, UserData


logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
formatter = logging.Formatter(
    "[{levelname}] {asctime}: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
console_handler.setFormatter(formatter)
registrator = StepikCourseRegistration(logger)
strategy = RandomUserAcquisition()
registration_pattern = BaseRegistrationPattern()
registration_pattern.set_batch_size(1)
# registration_pattern.set_interval()
# registration_pattern.set_interval_between_batches()

print(registration_pattern.get_next_batch_size())
print(registration_pattern.get_next_interval())
print(registration_pattern.get_next_interval_between_batches())


registrator.run(
    strategy,
    registration_pattern,
    [
        "194561",
        "131194",
        "195274",
        "132752",
        "107397",
        "122259",
        "170081",
        "102836",
        "176260",
        "172763",
        "139722",
    ],
)
# print(registrator.get_base_url())


# chrome_options = Options()
# DRIVER = webdriver.Chrome(
#     service=ChromeService(ChromeDriverManager().install()),
#     options=chrome_options,
# )

# DRIVER.get("https://stepik.org/registration")
