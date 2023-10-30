from src.abstractions.vacancy_provider import VacancyProvider, SearchResult
from src.abstractions.currency_provider import CurrencyProvider
from src.entities.currency import Currency
from src.providers.currency_provider_cbr import CurrencyProviderCBR


class VacancyComposer:
    """
    Compose a vacancy search results from multiple providers
    """

    def __init__(self,
                 vacancy_providers: list[VacancyProvider],
                 currency_provider: CurrencyProvider = None
                 ):
        """
        :param vacancy_providers: List of vacancy provider instance
        :param currency_provider: Currency provider class
        """
        if not currency_provider:
            currency_provider = CurrencyProviderCBR

        Currency.currency_provider = currency_provider
        self._providers = vacancy_providers

    def get_vacancies(
            self,
            search_text=None,
            page_num=None,
            per_page=None,
            providers: list[str] = None, **kwargs
    ) -> dict[str, SearchResult]:
        """
        Search vacancies from multiple providers
        :param search_text: Keyword
        :param page_num: Number of page
        :param per_page: Results per page
        :param providers: List of providers for search
        :param kwargs:
        :return:
        """

        if providers:
            providers = [s.lower().replace(' ', '') for s in providers]

        return dict(
            (
                provider.provider_name,
                provider.get_vacancies(search_text=search_text, page_num=page_num, per_page=per_page, **kwargs)
            )
            for provider in self._providers if providers is None or
            provider.provider_name.lower().replace(' ', '') in providers
        )

    @property
    def provider_names(self) -> list[str]:
        return [n.provider_name for n in self._providers]