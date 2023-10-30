from src.entities.salary import Salary


class Vacancy:

    def __init__(
            self,
            title: str,
            description: str = None,
            salary: Salary = None,
            url: str = None,
            provider_vacancy_id: int = None,
            company: str = None,
            city: str = None,
            provider: str = None
    ):
        self._salary = salary
        self._description = description
        self._title = title
        self._url = url
        self._provider_vacancy_id = provider_vacancy_id
        self._company = company
        self._city = city
        self._provider = provider

    def __eq__(self, other):
        if issubclass(other.__class__, self.__class__):
            return (self.title == other.title and
                    self.url == other.url and
                    self.description == other.description and
                    self.salary == other.salary)
        return False

    def __lt__(self, other):
        if self.salary is None:
            return True
        if issubclass(other.__class__, self.__class__):
            return self.salary < other.salary

    def __le__(self, other):
        if self.salary is None:
            return True
        if issubclass(other.__class__, self.__class__):
            return self.salary <= other.salary

    def __str__(self):

        if self.salary is not None:
            s = str(self.salary)
            s = f' Зарплата: {s if s else "Не указано"}'
        else:
            s = ''
        return f'{self.title}{s}'

    @property
    def salary(self) -> Salary | None:
        return self._salary

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def provider_vacancy_id(self):
        return self._provider_vacancy_id

    @property
    def company(self):
        return self._company

    @property
    def city(self):
        return self._city

    @property
    def provider(self):
        return self._provider
