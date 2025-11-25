from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Django AppConfig for the search app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.search"
    verbose_name = "Search"
