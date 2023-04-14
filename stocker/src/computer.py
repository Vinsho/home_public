from django.db.models import Q

from stocker.src.openAI import OpenAIClient
from stocker.src.scrapers.yahoo_scraper import YahooScraper
from stocker.models import Stock


class Computer:
    def __init__(self) -> None:
        self.scraper = YahooScraper()
        self.client = OpenAIClient()

    def split_result(self, result):
        if ', ' in result:
            return result.split(', ')
        else:
            return result.split(',')

    def compute_stock(self, stock: Stock):
        news = self.scraper.get_news(stock)

        if not news:
            return

        result = self.client.query(stock, news)
        impact_list = self.split_result(result)

        for news, impact in zip(news, impact_list):
            news.impact = impact
            news.save()

    def compute_all(self):
        for stock in Stock.objects.all():
            self.compute_stock(stock)
