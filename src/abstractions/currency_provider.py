from abc import abstractmethod, ABC

from src.abstractions.http_request_provider import HttpRequested


class CurrencyProvider(ABC, HttpRequested):
    """
    Provide methods for currency operations
    """

    @classmethod
    @abstractmethod
    def convert_currency(cls, value: float, from_curr: str, to_curr: str):
        pass

    @staticmethod
    def currency_code_parse(code: str):
        if len(code) != 3:
            raise ValueError("wrong currency code")
        return code.upper()