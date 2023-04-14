from django.urls import path

from . import views


urlpatterns = [
    path('klcovany/', views.PlantView.as_view(), name='klcovany'),
    path('', views.HomeView.as_view(), name='home'),
]
