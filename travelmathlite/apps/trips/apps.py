from django.apps import AppConfig


class TripsConfig(AppConfig):
    """Django AppConfig for the trips app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.trips"
    verbose_name = "Trips"
