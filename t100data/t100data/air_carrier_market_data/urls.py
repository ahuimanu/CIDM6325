# urls.py
from django.urls import path
from . views import MarketDataList

urlpatterns = [
    path('list/', MarketDataList.as_view()),
]