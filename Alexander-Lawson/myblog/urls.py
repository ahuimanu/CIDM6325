from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_list, name="blog_list"),  # Double quotes used here
]