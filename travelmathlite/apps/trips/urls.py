from django.urls import path

from .views import IndexView, SavedCalculationDeleteView, SavedCalculationListView

app_name = "trips"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("saved/", SavedCalculationListView.as_view(), name="saved_list"),
    path(
        "saved/<int:pk>/delete/",
        SavedCalculationDeleteView.as_view(),
        name="saved_delete",
    ),
]
