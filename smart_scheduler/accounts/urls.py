from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

from django.urls import path

app_name = "accounts"

urlpatterns = [
    # add paths later, e.g. path("profile/", views.profile, name="profile"),
]
