from django.urls import path

from .views import IndexView

app_name = "airports"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
