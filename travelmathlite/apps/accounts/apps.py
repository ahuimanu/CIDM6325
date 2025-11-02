from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django AppConfig for the accounts app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Accounts"
