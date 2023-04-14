from django.contrib import admin

from .models import Stock, News
# Register your models here.

admin.site.register(Stock)
admin.site.register(News)
