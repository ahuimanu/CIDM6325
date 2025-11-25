from django.apps import AppConfig


class AirportsConfig(AppConfig):
    """Django AppConfig for the airports app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.airports"
    verbose_name = "Airports"
