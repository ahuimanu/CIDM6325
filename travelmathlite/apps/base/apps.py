from django.apps import AppConfig


class BaseConfig(AppConfig):
    """Django AppConfig for the base app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.base"
    verbose_name = "Base"
