from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core import views as core_views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", RedirectView.as_view(pattern_name="blog:post_list", permanent=False)),
    path("admin/", admin.site.urls),

    # 👇 our GET/POST logout
    path("accounts/logout/", core_views.GetLogoutView.as_view(), name="logout"),


    # built-in auth (login, password-reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),

    # our custom register page
    path("accounts/register/", core_views.register, name="register"),

    
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





