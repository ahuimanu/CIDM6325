from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)


app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
