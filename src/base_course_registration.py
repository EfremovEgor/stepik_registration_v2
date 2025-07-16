from abc import ABC, abstractmethod
from logging import Logger

from registration_patterns import BaseRegistrationPattern
from users_acquisition import BaseUserAcquisition


class BaseCourseRegistration(ABC):
    logger: Logger | None
    total_registered: int = 0

    def __init__(self, logger: Logger | None):
        self.logger = logger

    def log(self, level: int, message: str):
        if self.logger is None:
            return
        self.logger.log(level, message)

    @abstractmethod
    def run(
        self,
        strategy: BaseUserAcquisition,
        registration_pattern: BaseRegistrationPattern,
        courses: list[str],
    ): ...

    @abstractmethod
    def get_base_url(self): ...
