from __future__ import annotations

from typing import Any

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from ..airports.models import Airport
from ..base.models import City


@method_decorator(cache_page(300), name="dispatch")  # 5 minutes
class SearchView(TemplateView):
    """Render search results for airports and cities based on `q`.

    Non-goals in this slice: pagination and highlighting (handled in later briefs).
    """

    template_name: str = "search/results.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        raw_q = self.request.GET.get("q", "")
        q = (raw_q or "").strip()

        context["query"] = q
        context["had_query"] = bool(q)

        if not q:
            # Avoid DB work on empty queries
            context["airport_results"] = Airport.objects.none()
            context["city_results"] = City.objects.none()
            context["results"] = []
            context["results_count"] = 0
            context["page_obj"] = None
            return context

        # Basic icontains search using existing queryset helpers; limit until pagination lands
        airports: QuerySet[Airport] = (
            Airport.objects.search(q)
            .select_related("country", "city")
            .only(
                "name",
                "iata_code",
                "ident",
                "municipality",
                "iso_country",
                "country__name",
                "city__name",
            )
        )
        cities: QuerySet[City] = (
            City.objects.search(q)
            .select_related("country")
            .only(
                "name",
                "slug",
                "country__iso_code",
                "country__name",
            )
        )

        # Combine into a single list for pagination; airports first, then cities (simple deterministic grouping)
        combined: list[tuple[str, object]] = [("airport", a) for a in airports] + [("city", c) for c in cities]

        paginator = Paginator(combined, 20)
        page_number = self.request.GET.get("page")
        page_obj: Page = paginator.get_page(page_number)

        context["airport_results"] = []  # deprecated in favor of combined paginator
        context["city_results"] = []
        context["results"] = page_obj.object_list
        context["results_count"] = paginator.count
        context["page_obj"] = page_obj
        return context
