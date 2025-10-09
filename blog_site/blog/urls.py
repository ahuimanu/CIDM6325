from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),    
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.post_update, name="post_update"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]