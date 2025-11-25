from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django AppConfig for the accounts app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Accounts"

    def ready(self) -> None:
        """
        Import signal handlers when app is ready.

        This ensures that signal receivers are registered when Django starts.
        """
        from . import signals  # noqa: F401
