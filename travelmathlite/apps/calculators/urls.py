from django.urls import path

from .views import CostCalculatorView, CostPartialView, DistanceCalculatorView, DistancePartialView, IndexView

app_name = "calculators"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("distance/", DistanceCalculatorView.as_view(), name="distance"),
    # Partial endpoints used by HTMX/tests; reuse same CBVs
    path("distance/partial/", DistancePartialView.as_view(), name="distance-partial"),
    path("cost/", CostCalculatorView.as_view(), name="cost"),
    path("cost/partial/", CostPartialView.as_view(), name="cost-partial"),
]
