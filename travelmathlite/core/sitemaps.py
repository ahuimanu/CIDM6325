"""Sitemaps for TravelMathLite."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static/key views."""

    priority = 0.5
    changefreq = "daily"

    def items(self):
        """Return list of static view names."""
        return [
            "base:index",
            "search:index",
            "airports:index",
            "airports:nearest",
            "calculators:index",
        ]

    def location(self, item):
        """Return URL for each view."""
        return reverse(item)
