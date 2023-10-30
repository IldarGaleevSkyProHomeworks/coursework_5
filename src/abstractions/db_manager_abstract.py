from abc import ABC, abstractmethod

from src.entities.vacancy import Vacancy


class DBManagerAbstract(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> dict:
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[Vacancy]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[Vacancy]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keywords: list[str]) -> list[Vacancy]:
        pass

    @abstractmethod
    def insert_vacancies(self, vacancies: list[Vacancy]):
        pass
