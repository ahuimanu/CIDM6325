from __future__ import annotations

from typing import Any

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import FormView, TemplateView

from .costs import calculate_fuel_cost
from .forms import CostCalculatorForm, DistanceCalculatorForm
from .geo import calculate_distance_between_points


class IndexView(TemplateView):
    """Minimal index landing page for the Calculators app."""

    template_name: str = "calculators/index.html"


@method_decorator(cache_page(600), name="dispatch")  # 10 minutes
class DistanceCalculatorView(FormView):
    template_name = "calculators/distance_calculator.html"
    form_class = DistanceCalculatorForm

    def form_valid(self, form: DistanceCalculatorForm) -> HttpResponse:  # type: ignore[override]
        lat1, lon1 = form.origin_coords
        lat2, lon2 = form.destination_coords
        unit = form.cleaned_data["unit"].lower()
        route_factor = float(form.cleaned_data["route_factor"])  # already validated

        flight, driving = calculate_distance_between_points(
            lat1, lon1, lat2, lon2, unit=unit, include_driving_estimate=True, route_factor=route_factor
        )

        # Driving time estimate (hours) using AVG_SPEED_KMH; if miles, convert speed
        avg_speed_kmh = float(getattr(settings, "AVG_SPEED_KMH", 80.0))
        driving_km = driving if unit == "km" else driving * 1.60934
        hours = driving_km / avg_speed_kmh if driving_km > 0 else 0.0

        context: dict[str, Any] = {
            "form": form,
            "unit": unit,
            "flight_distance": flight,
            "driving_distance": driving,
            "driving_time_hours": hours,
        }

        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "calculators/partials/distance_result.html", context)
        return render(self.request, self.template_name, context)

    def form_invalid(self, form: DistanceCalculatorForm) -> HttpResponse:  # type: ignore[override]
        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "calculators/partials/distance_result.html", {"form": form}, status=400)
        return super().form_invalid(form)


@method_decorator(cache_page(600), name="dispatch")  # 10 minutes
class CostCalculatorView(FormView):
    template_name = "calculators/cost_calculator.html"
    form_class = CostCalculatorForm

    def form_valid(self, form: CostCalculatorForm) -> HttpResponse:  # type: ignore[override]
        lat1, lon1 = form.origin_coords
        lat2, lon2 = form.destination_coords
        unit = form.cleaned_data["unit"].lower()
        route_factor = float(form.cleaned_data["route_factor"])  # already validated

        flight, driving = calculate_distance_between_points(
            lat1, lon1, lat2, lon2, unit=unit, include_driving_estimate=True, route_factor=route_factor
        )

        # Cost is computed on kilometers; convert if user selected miles
        driving_km = driving if unit == "km" else driving * 1.60934
        fuel_economy = float(form.cleaned_data["fuel_economy_l_per_100km"])  # L/100km
        fuel_price = float(form.cleaned_data["fuel_price_per_liter"])  # currency per liter
        total_cost = calculate_fuel_cost(driving_km, fuel_economy_l_per_100km=fuel_economy, fuel_price_per_liter=fuel_price)

        # Driving time estimate
        avg_speed_kmh = float(getattr(settings, "AVG_SPEED_KMH", 80.0))
        hours = driving_km / avg_speed_kmh if driving_km > 0 else 0.0

        context: dict[str, Any] = {
            "form": form,
            "unit": unit,
            "flight_distance": flight,
            "driving_distance": driving,
            "driving_time_hours": hours,
            "fuel_cost": total_cost,
        }

        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "calculators/partials/cost_result.html", context)
        return render(self.request, self.template_name, context)

    def form_invalid(self, form: CostCalculatorForm) -> HttpResponse:  # type: ignore[override]
        if self.request.headers.get("HX-Request") == "true":
            return render(self.request, "calculators/partials/cost_result.html", {"form": form}, status=400)
        return super().form_invalid(form)


class DistancePartialView(DistanceCalculatorView):
    def form_invalid(self, form: DistanceCalculatorForm) -> HttpResponse:  # type: ignore[override]
        # For partial endpoint, on invalid input render full page with errors (tests expect this)
        return render(self.request, "calculators/distance_calculator.html", {"form": form}, status=400)


class CostPartialView(CostCalculatorView):
    def form_invalid(self, form: CostCalculatorForm) -> HttpResponse:  # type: ignore[override]
        # For partial endpoint, on invalid input render full page with errors (tests expect this)
        return render(self.request, "calculators/cost_calculator.html", {"form": form}, status=400)
