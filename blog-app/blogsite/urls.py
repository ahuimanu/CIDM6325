from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from blog import views as blog_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Custom login view first so we can handle POST and messages clearly
    path("accounts/login/", blog_views.login_view, name="login"),
    # Keep the rest of the auth routes (logout, password reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("blog.urls")),   # <-- this brings in the root mapping
]
