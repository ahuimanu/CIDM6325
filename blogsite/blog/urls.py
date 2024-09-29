from django.urls import path
from .feeds import LatestPostsFeed
from . import views

# app_name is a variable that Django uses to further specify urls with an app_name prefix.
app_name = "blog"
urlpatterns = [
    # post views
    # https://myblog.com/blog/
    path("", views.post_list, name="post_list"),
    # path("", views.PostListView.as_view(), name="post_list"),
    # path("<int:id>/", views.post_detail, name="post_detail"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post_slug>/",
        views.post_detail,
        name="post_detail",
    ),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("feed/", LatestPostsFeed(), name="post_feed"),
    path("search/", views.post_search, name="post_search"),
]

# https://myblog.com/blog/
