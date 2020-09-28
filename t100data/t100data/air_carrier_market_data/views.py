# Create your views here.
from django.views.generic import ListView
from django.db.models import Max, Sum

from . models import MarketData

class MarketDataList(ListView):
    model = MarketData

# What are the top 5 airports in terms of: Total passengers by origin
class Top5AirportsPaxByOrigin(ListView):
    context_object_name = "airport_list"
    queryset = MarketData.objects.values('orig_iata_code','orig_city_name') \
                                 .annotate(total_pax=Sum('passengers')) \
                                 .order_by('-total_pax')[0:5]
    template_name="rankorder_list_origin.html"

# What are the top 5 airports in terms of: Total passengers by destination
class Top5AirportsPaxByDestination(ListView):
    context_object_name = "airport_list"
    queryset = MarketData.objects.values('dest_iata_code','dest_city_name') \
                                 .annotate(total_pax=Sum('passengers')) \
                                 .order_by('-total_pax')[0:5]
    template_name="rankorder_list_destination.html"


# Which airport reported the longest distance by month?
class TopDistanceByMonth(ListView):
    context_object_name = "airport_list"
    queryset = MarketData.objects.filter() \
                                 .values('orig_iata_code','orig_city_name','dest_iata_code','dest_city_name') \
                                 .annotate(total_distance=Max('distance')) \
                                 .order_by('-total_distance')[0:5]
#                                .order_by('month')[0:5]

    template_name="rankorder_list_origin_distance_month.html"