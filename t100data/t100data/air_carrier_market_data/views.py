# Create your views here.
from django.views.generic import ListView
from . models import MarketData

class MarketDataList(ListView):
    model = MarketData