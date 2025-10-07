from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostList.as_view(), name="post_list"),
    path("new/", views.PostCreate.as_view(), name="post_create"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("<slug:slug>/edit/", views.PostUpdate.as_view(), name="post_update"),
    path("<slug:slug>/delete/", views.PostDelete.as_view(), name="post_delete"),
]
