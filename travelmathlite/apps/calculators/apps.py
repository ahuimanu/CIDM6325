from django.apps import AppConfig


class CalculatorsConfig(AppConfig):
    """Django AppConfig for the calculators app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.calculators"
    verbose_name = "Calculators"
