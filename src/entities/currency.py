from src.abstractions.currency_provider import CurrencyProvider


class Currency:
    base_currency = 'RUB'
    currency_provider: CurrencyProvider = None
    """ Currency convert provider """

    def __init__(self, value: float, code: str):
        """
        Currency
        :param value: Currency value
        :param code: Currency code (ISO 4217 alpha-3)
        """

        self._value = float(value)
        self._currency_code = CurrencyProvider.currency_code_parse(code)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._value},code={self._currency_code})"

    def __str__(self):
        return f"{self.value} {self.code}"

    def __getitem__(self, code) -> float:
        """
        Returns converted currency value by currency code (ISO 4217)
        :param code: Currency code: alpha-3 (ex. USD)
        :return:
        """

        if self.currency_provider is None:
            raise ReferenceError("Currency converter not assigned")

        code = CurrencyProvider.currency_code_parse(code)
        return self.currency_provider.convert_currency(self.value, self.code, code)

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__):
            return self[self.base_currency] == other[self.base_currency]
        return False

    def __lt__(self, other):
        if issubclass(other.__class__, self.__class__):
            return self[self.base_currency] < other[self.base_currency]
        raise TypeError("Can`t compare")

    def __le__(self, other):
        if issubclass(other.__class__, self.__class__):
            return self[self.base_currency] <= other[self.base_currency]
        raise TypeError("Can`t compare")

    @property
    def value(self):
        return round(self._value,2)

    @property
    def code(self):
        return self._currency_code


MIN_CURRENCY = Currency(0.0, Currency.base_currency)
MAX_CURRENCY = Currency(float('inf'), Currency.base_currency)