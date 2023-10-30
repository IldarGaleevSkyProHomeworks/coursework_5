from src.entities.currency import Currency, MIN_CURRENCY, MAX_CURRENCY


class Salary:
    def __init__(self, salary_from: Currency = None, salary_to: Currency = None):
        self.__from = salary_from
        self.__to = salary_to

    @property
    def salary_from(self) -> Currency | None:
        return self.__from

    @property
    def salary_to(self) -> Currency | None:
        return self.__to

    def __get_range(self):
        if self.__from is None and self.__to is None:
            return MIN_CURRENCY, MIN_CURRENCY

        low = self.__to if self.__from is None else self.__from
        high = self.__from  if self.__to is None else self.__to

        return low, high

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__):
            return (self.salary_from == other.salary_from and
                    self.salary_to == other.salary_to)

    def __lt__(self, other):
        if other is None:
            return False

        if not issubclass(other.__class__, self.__class__):
            raise TypeError("Can`t compare this objects")

        l1, h1 = self.__get_range()
        l2, h2 = other.__get_range()

        return l1 < l2 or h1 < h2

    def __le__(self, other):
        if other is None:
            return False

        if not issubclass(other.__class__, self.__class__):
            raise TypeError("Can`t compare this objects")

        l1, h1 = self.__get_range()
        l2, h2 = other.__get_range()

        return l1 <= l2 or h1 <= h2

    def __str__(self):
        res = '' if self.salary_from is None else f'от {str(self.salary_from)}'
        res += '' if self.salary_to is None else f' до {str(self.salary_to)}'

        return res.lstrip()
