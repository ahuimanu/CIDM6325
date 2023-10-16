from django.urls import path
from .views import dashboard

app_name = "blabber"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]