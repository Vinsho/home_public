from langchain.llms import OpenAIChat
from dotenv import load_dotenv

from stocker.models import News, Stock


class OpenAIClient:
    def __init__(self) -> None:
        load_dotenv()
        self.model = OpenAIChat(model_name="gpt-3.5-turbo")
        self._separator = "\n-----\n"

    def get_prompt(self, stock):
        return f"""Try to act as an investor. How much of an impact do each of the following news have on {stock} stock ?
Give a number on scale from -10 to 10, where -10 is a negative impact that will result in a massive price drop and 10 is a positive impact that will result in massive price increase.
Return only the numbers in form of a list of values separated by ','. No other tokens. News are separated by {self._separator}"""

    def query(self, stock: Stock, news_list: list[News]):
        news_list = [news.get_text() for news in news_list]
        query = self.get_prompt(stock.ticker) + self._separator.join(news_list)
        return self.model(query)
