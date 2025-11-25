from django.urls import path

from .views import IndexView, NearestAirportView, nearest_airports_json

app_name = "airports"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("nearest/", NearestAirportView.as_view(), name="nearest"),
    path("api/nearest", nearest_airports_json, name="nearest_json"),
]
