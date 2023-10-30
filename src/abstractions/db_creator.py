from abc import abstractmethod
from typing import Dict


class ConfirmationException(Exception):
    pass


class DBCreatorProp:
    def __init__(self, description: str, default: str | None, secure: bool = False, validate_cb=None):
        self._description = description
        self._value = default
        self._validate = validate_cb
        self._secure = secure

    def __str__(self):
        return '***' if self._secure else str(self._value)

    @property
    def description(self):
        return self._description

    @property
    def value(self):
        return self._value

    @property
    def secure(self):
        return self._secure

    @value.setter
    def value(self, value):
        if self._validate:
            self._validate(value)
        self._value = value

    @staticmethod
    def digit_validate(value: str):
        if not value.isdigit():
            raise TypeError(f'Value must be a numeric')

    @staticmethod
    def empty_validate(value: str):
        if not value:
            raise ConfirmationException(f'Value is empty!')

    @staticmethod
    def not_eq_validate(c_value, message: str):
        def _check(value):
            if value == c_value:
                raise ConfirmationException(message)

        return _check


class DBCreator:

    def __init__(self):
        self._db_props: Dict[str, DBCreatorProp] = {}

    def __iter__(self):
        return iter(self._db_props.values())

    @abstractmethod
    def init_database(self):
        pass
