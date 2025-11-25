from __future__ import annotations

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from .forms import NearestAirportForm
from .models import Airport


class IndexView(TemplateView):
    """Minimal index landing page for the Airports app."""

    template_name: str = "airports/index.html"


class NearestAirportView(FormView):
    """Render simple page to search nearest airports using the form.

    GET: show empty form
    POST: validate and display top results
    HTMX POST: return only the results partial
    """

    template_name = "airports/nearest.html"
    form_class = NearestAirportForm

    def form_valid(self, form: NearestAirportForm) -> HttpResponse:
        latitude, longitude = form.resolved_coords  # type: ignore[misc]
        unit = form.cleaned_data.get("unit", "km")
        limit = form.cleaned_data.get("limit", 3)
        iso_country = form.cleaned_data.get("iso_country") or None
        results = Airport.objects.nearest(latitude, longitude, limit=limit, unit=unit, iso_country=iso_country)

        # If HTMX request, return only the partial template
        if self.request.headers.get("HX-Request"):
            return render(self.request, "airports/partials/nearest_results.html", {"results": results, "unit": unit})

        context = self.get_context_data(form=form, results=results, unit=unit)
        return self.render_to_response(context)

    def form_invalid(self, form: NearestAirportForm) -> HttpResponse:
        # If HTMX request and form is invalid, return error message in partial
        if self.request.headers.get("HX-Request"):
            return render(self.request, "airports/partials/nearest_results.html", {"results": None})
        return self.render_to_response(self.get_context_data(form=form, results=None))


def nearest_airports_json(request: HttpRequest) -> JsonResponse:
    """Return nearest airports JSON given query parameters.

    Params: q, iso_country, unit (km/mi), limit (1-10)
    """
    data = {
        "query": request.GET.get("q", ""),
        "iso_country": request.GET.get("iso_country", ""),
        "unit": request.GET.get("unit", "km"),
        "limit": request.GET.get("limit", ""),
    }
    form = NearestAirportForm(data=data)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=400)

    latitude, longitude = form.resolved_coords  # type: ignore[misc]
    unit = form.cleaned_data.get("unit", "km")
    limit = form.cleaned_data.get("limit", 3)
    iso_country = form.cleaned_data.get("iso_country") or None
    results = Airport.objects.nearest(latitude, longitude, limit=limit, unit=unit, iso_country=iso_country)

    payload = {
        "count": len(results),
        "unit": unit,
        "results": [
            {
                "ident": a.ident,
                "iata": a.iata_code,
                "name": a.name,
                "distance": getattr(a, "distance_mi", None) if unit == "mi" else getattr(a, "distance_km", None),
            }
            for a in results
        ],
    }
    return JsonResponse(payload)
