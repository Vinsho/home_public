import requests
from django.db.models import Q
from bs4 import BeautifulSoup
from stocker.models import News, Stock

from stocker.src.scrapers.scraper import Scraper


class YahooScraper(Scraper):
    def get_stock_url(self, stock):
        return "https://finance.yahoo.com/quote/" + stock.ticker

    def get_news(self, stock: Stock) -> list[News]:
        page = requests.get(self.get_stock_url(stock))
        soup = BeautifulSoup(page.content, "html.parser")
        news_list = soup.find_all("li", class_="js-stream-content Pos(r)")

        result = []

        for news in news_list:
            title = news.find('h3').text
            description = news.find('p').text
            url = 'https://finance.yahoo.com' + news.find('h3').find('a', href=True)['href']

            if News.objects.filter(Q(url=url)):
                continue

            news = News(title=title, description=description, url=url, stock=stock)
            news.save()

            result.append(news)

        return result
