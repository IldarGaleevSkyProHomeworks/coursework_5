from abc import abstractmethod, ABC

from src.abstractions.http_request_provider import HttpRequested
from src.entities.vacancy import Vacancy
from typing import NamedTuple


class SearchResult(NamedTuple):
    result_list: list[Vacancy]
    total_pages: int
    total_results: int
    page_num: int


class VacancyProvider(ABC, HttpRequested):
    """
    Provide methods for search vacancies
    """

    @abstractmethod
    def get_vacancies(self, search_text=None, page_num=None, per_page=None, **kwargs) -> SearchResult:
        """
        Get vacancies list

        :param search_text: text for search
        :param page_num: page number
        :param per_page: results per page

        :return:
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass
