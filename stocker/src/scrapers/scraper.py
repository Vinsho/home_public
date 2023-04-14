from abc import ABC, abstractmethod, abstractproperty
from stocker.models import News, Stock


class Scraper(ABC):
    @abstractmethod
    def get_news(self, stock: Stock) -> list[News]:
        pass

    @abstractmethod
    def get_stock_url(self, stock: Stock):
        pass
