from django.urls import path

from . import views


urlpatterns = [
    path('stocker/', views.StockerView.as_view(), name='stocker'),
    path('stocks/', views.StocksView.as_view(), name='stocks'),
    path('stocks/<str:ticker>', views.StockView.as_view(), name='stock'),
]
