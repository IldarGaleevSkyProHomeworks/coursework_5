from abc import abstractmethod, ABC


class HttpRequestProvider(ABC):
    """
    Provide json data by url
    """

    @classmethod
    @abstractmethod
    def get_data_dict(cls, url: str, **kwargs) -> dict:
        pass


class HttpRequested:
    """
    Require http request
    """
    http_request_provider: HttpRequestProvider = None
