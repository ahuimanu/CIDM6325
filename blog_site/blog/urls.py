from django.urls import path

from .feeds import LatestPostsAtomFeed, LatestPostsRSSFeed
from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    # Feeds
    path("feeds/rss/", LatestPostsRSSFeed(), name="feed_rss"),
    path("feeds/atom/", LatestPostsAtomFeed(), name="feed_atom"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
