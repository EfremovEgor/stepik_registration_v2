from abc import ABC, abstractmethod
from code import interact
from typing import Callable, TypedDict


class BaseRegistrationPattern:
    total_to_register: int
    interval: int | None
    interval_generator: Callable[[], int] | None
    batch_size: int
    batch_size_generator: Callable[[], int] | None
    interval_between_batches: int | None
    interval_between_batches_generator: Callable[[], int] | None

    max_attempts_to_register: int = 5
    max_attempts_to_login: int = 5
    max_attempts_to_enroll: int = 5

    def __init__(self, total_to_register: int):
        self.total_to_register = total_to_register
        self.interval = None
        self.interval_generator = None
        self.batch_size = 1
        self.batch_size_generator = None
        self.interval_between_batches = None
        self.interval_between_batches_generator = None

    def set_interval(self, value: int | None | Callable[[], int]):
        if isinstance(value, int) or value is None:
            self.interval = value
            self.interval_generator = None
            return
        self.interval = None
        self.interval_generator = value

    def set_interval_between_batches(self, value: int | None | Callable[[], int]):
        if isinstance(value, int) or value is None:
            self.interval_between_batches = value
            self.interval_between_batches_generator = None
            return
        self.interval_between_batches = None
        self.interval_between_batches_generator = value

    def set_batch_size(self, value: int | Callable[[], int]):
        if isinstance(value, int):
            self.batch_size = value
            self.batch_size_generator = None
            return
        self.batch_size = None
        self.batch_size_generator = value

    def get_total_to_register(self):
        return self.total_to_register

    def get_next_batch_size(self) -> int:
        if self.batch_size is not None:
            return self.batch_size
        return self.batch_size_generator()

    def get_next_interval(self) -> int | None:
        if self.interval is not None:
            return self.interval
        if self.interval_generator is not None:
            return self.interval_generator()
        return None

    def get_next_interval_between_batches(self) -> int | None:
        if self.interval_between_batches is not None:
            return self.interval
        if self.interval_between_batches_generator is not None:
            return self.interval_between_batches_generator()
        return None
