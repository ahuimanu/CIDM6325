from django.urls import path
from . import views

# app_name is a variable that Django uses to further specify urls with an app_name prefix.
app_name = "blog"
urlpatterns = [
    # post views
    # https://myblog.com/blog/
    # path("", views.post_list, name="post_list"),
    path("", views.PostListView.as_view(), name="post_list"),
    # path("<int:id>/", views.post_detail, name="post_detail"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post_slug>/",
        views.post_detail,
        name="post_detail",
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]

# https://myblog.com/blog/
