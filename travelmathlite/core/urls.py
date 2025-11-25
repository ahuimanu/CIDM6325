"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import StaticViewSitemap
from .views import health_check

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    # Health check endpoint
    path("health/", health_check, name="health"),
    # Namespaced app URLs
    path("", include("apps.base.urls", namespace="base")),
    path("calculators/", include("apps.calculators.urls", namespace="calculators")),
    path("airports/", include("apps.airports.urls", namespace="airports")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("trips/", include("apps.trips.urls", namespace="trips")),
    path("search/", include("apps.search.urls", namespace="search")),
    # SEO
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]
