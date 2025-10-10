from django.urls import path
from . import views

urlpatterns = [
    # list & detail
    path("", views.PostListView.as_view(), name="post_list"),
    # CRUD - static routes first to avoid slug conflicts
    path("posts/new/", views.post_create, name="post_create"),
    path("posts/review/", views.review_list, name="review_list"),
    path("debug/users/", views.debug_users, name="debug_users"),
    path("debug/users/reset/<str:username>/", views.debug_reset_password, name="debug_reset_password"),
    path("posts/<slug:slug>/edit/", views.post_update, name="post_update"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    # detail (dynamic slug) - placed after static routes
    path("posts/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),

    # HTMX endpoints
    path("hx/search/", views.hx_post_search, name="hx_post_search"),
    path("hx/posts/<int:pk>/inline/", views.hx_post_inline_edit, name="hx_post_inline_edit"),
    # Development-only helper to create/login a dev user when DEBUG=True
    path("dev-login/", views.dev_login, name="dev_login"),
    path("accounts/register/", views.register, name="register"),
    path("posts/review/", views.review_list, name="review_list"),
]
