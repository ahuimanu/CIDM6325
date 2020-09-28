from django.urls import path, include

# from django.contrib.auth import views as auth_views

from . views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]