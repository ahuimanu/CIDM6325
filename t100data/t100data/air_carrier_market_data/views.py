# Create your views here.
from django.views.generic import ListView
from . models import MarketData

class MarketDataList(ListView):
    model = MarketData

class Top5AirportsPaxByOrigin(ListView):
    model = MarketData
    template_name="Top5AirportsPaxByOrigin_list.html"