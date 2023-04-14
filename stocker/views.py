import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from stocker.models import News, Stock
from stocker.src.computer import Computer

# Create your views here.
STOCKER_SELECTION_AGE = 3
POSITIVE_NEWS_THRESH = 8
NEGATIVE_NEWS_THRESH = -7


class StocksView(LoginRequiredMixin, View):
    template = "stocker/stocks.html"

    def get(self, request):
        stocks = Stock.objects.all()
        return render(request, self.template, {'stocks': stocks})

    def post(self, request):
        if not Stock.objects.filter(ticker=request.POST.get('ticker')):
            Stock(ticker=request.POST.get('ticker')).save()

        return redirect(request.META['HTTP_REFERER'])


class StockerView(LoginRequiredMixin, View):
    template = "stocker/stocker.html"

    def get(self, request):
        date_from = datetime.datetime.now() - datetime.timedelta(days=STOCKER_SELECTION_AGE)
        positive_news = News.objects.order_by(
            '-datetime').filter(Q(datetime__gte=date_from, impact__gte=POSITIVE_NEWS_THRESH))
        negative_news = News.objects.order_by(
            '-datetime').filter(Q(datetime__gte=date_from, impact__lte=NEGATIVE_NEWS_THRESH))

        return render(request, self.template, {'positive_news': positive_news, 'negative_news': negative_news})


class StockView(LoginRequiredMixin, View):
    template = "stocker/stock.html"

    def get(self, request, ticker):
        stock = Stock.objects.filter(Q(ticker=ticker)).first()

        computer = Computer()
        computer.compute_stock(stock)

        ordered_news = stock.news.order_by('-datetime')

        context = {
            'stock': stock,
            'negative_news': [news for news in ordered_news if news.impact < 0],
            'positive_news': [news for news in ordered_news if news.impact >= 0]
        }

        return render(request, self.template, context)
