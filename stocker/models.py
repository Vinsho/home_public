import datetime
from django.db import models
from django.db.models import Q


class Stock(models.Model):
    ticker = models.CharField(max_length=16)

    def day_avg_rating(self):
        date_from = datetime.datetime.now() - datetime.timedelta(days=1)
        day_news = self.news.filter(Q(datetime__gte=date_from))
        if not day_news:
            return 0
        return round(sum(news.impact for news in day_news) / len(day_news), 1)


class News(models.Model):
    url = models.TextField()
    title = models.TextField()
    description = models.TextField()
    impact = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, related_name="news")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_text(self):
        return f"{self.title} \n {self.description}"

    def __str__(self):
        return f"""
        Stock: {self.stock}
        News: {self.description}
        Url: {self.url}
        Time: {self.time}
        Impact: {self.impact}\n
        """
