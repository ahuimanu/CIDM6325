# Tutorial: ADR-1.0.2 Distance & Cost Calculators

## Goal

Learn how TravelMathLite implements distance (haversine and geodesic) and cost estimation calculators, including form validation, Django settings integration, and HTMX-driven UI updates.

## Context

- **ADR:** `docs/travelmathlite/adr/adr-1.0.2-geo-calculation-methods.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.2/` (six briefs covering algorithms → settings → costs → forms → views → docs)
- **App:** `travelmathlite/apps/calculators/`
- **Algorithm Documentation:** `docs/travelmathlite/algorithms/distance-and-cost.md`

## Prerequisites

- TravelMathLite project initialized with `uv`
- Python environment activated
- Database migrated
- Basic familiarity with Django forms, views, settings, and templates

## Section 1: Core Distance Algorithms (Brief 01)

### Brief Context

Implement core distance calculation functions: haversine (spherical approximation), geodesic (ellipsoidal, via geopy), unit conversions, and driving distance estimation.

### Django and Python Concepts

**From Matt Layman's "Understand Django" (Chapter: Settings and Configuration):**

> Django apps often need utility functions that don't belong in models or views. Create a separate module (e.g., `utils.py` or `geo.py`) for these helpers. Keep them pure functions when possible so they're easy to test.

**Mathematical Background:**

**Haversine Formula** (great-circle distance on a sphere):

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1−a))
distance = R × c
```

Where R = 6371 km (Earth's mean radius).

**Geodesic Distance** (ellipsoidal Earth model):

- More accurate for long distances (< 0.15% error vs. < 0.5% for haversine)
- Requires iterative calculation (use `geopy.distance.geodesic`)

### Implementation Steps

**1. Create distance utility module**

File: `apps/calculators/geo.py`:

```python
"""Geographic distance and conversion utilities."""
import math
from typing import Literal

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute great-circle distance in kilometers using Haversine formula.
    
    Accurate within 0.5% for most distances. Fast and dependency-free.
    """
    R = 6371.0  # Earth radius in km
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def geodesic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute geodesic distance in kilometers using WGS-84 ellipsoid.
    
    More accurate than haversine (< 0.15% error). Requires geopy.
    """
    try:
        from geopy.distance import geodesic
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers
    except ImportError:
        return haversine_distance(lat1, lon1, lat2, lon2)

def km_to_miles(km: float) -> float:
    """Convert kilometers to statute miles."""
    return km * 0.621371

def miles_to_km(miles: float) -> float:
    """Convert statute miles to kilometers."""
    return miles / 0.621371

def estimate_driving_distance(flight_km: float, route_factor: float = 1.25) -> float:
    """Estimate driving distance from flight distance.
    
    Args:
        flight_km: Straight-line distance
        route_factor: Multiplier for roads (default 1.25 = 25% longer)
    
    Returns:
        Estimated driving distance in kilometers
    """
    return flight_km * route_factor

def calculate_distance_between_points(
    lat1: float, lon1: float, lat2: float, lon2: float,
    *,
    method: Literal["haversine", "geodesic"] = "haversine",
    unit: Literal["km", "mi"] = "km",
) -> float:
    """Unified distance calculation with method and unit selection."""
    if method == "geodesic":
        km = geodesic_distance(lat1, lon1, lat2, lon2)
    else:
        km = haversine_distance(lat1, lon1, lat2, lon2)
    
    return km_to_miles(km) if unit == "mi" else km
```

**2. Why these choices?**

- **Haversine default:** Fast, no dependencies, sufficient for most use cases
- **Geodesic fallback:** Use when precision matters (long distances, billing)
- **Route factor (1.25):** Heuristic for road vs. straight-line; adjustable per region
- **Pure functions:** Easy to test and compose

### Verification

```bash
# Django shell
uv run python travelmathlite/manage.py shell

>>> from apps.calculators.geo import haversine_distance, km_to_miles
>>> km = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)  # NYC to LA
>>> print(f"{km:.2f} km = {km_to_miles(km):.2f} mi")
3936.23 km = 2445.71 mi

# Run tests
uv run python travelmathlite/manage.py test apps.calculators.tests.test_geo
```

---

## Section 2: Settings and Defaults (Brief 02)

### Brief Context

Define project-wide defaults for route factors, driving speed, fuel prices, and fuel economy in Django settings.

### Django Concepts: Settings

**From Matt Layman's "Understand Django" (Chapter: Settings):**

> Django's settings module is where you configure your application. Use constants for business logic defaults (like pricing or conversion factors) so they can be changed without code edits. Access settings via `from django.conf import settings`.

**From Django Documentation:**

> **Custom Settings:** You can add your own settings to `settings.py`. Use uppercase names to distinguish them from variables. Access via `settings.YOUR_SETTING`.

### Implementation Steps

**1. Add calculator defaults to settings**

File: `core/settings.py`:

```python
# Distance and Cost Calculator Defaults
ROUTE_FACTOR = 1.25  # Driving distance = flight distance × route_factor
AVG_SPEED_KMH = 80  # Average driving speed in km/h
FUEL_PRICE_PER_LITER = 1.50  # Default fuel price (EUR/USD per liter)
FUEL_ECONOMY_L_PER_100KM = 8.0  # Default fuel consumption (liters per 100 km)

# Unit preferences
DEFAULT_DISTANCE_UNIT = "km"  # "km" or "mi"
DEFAULT_DISTANCE_METHOD = "haversine"  # "haversine" or "geodesic"
```

**2. Access in code**

```python
from django.conf import settings

def get_default_route_factor() -> float:
    return getattr(settings, "ROUTE_FACTOR", 1.25)
```

### Verification

```python
# Django shell
from django.conf import settings
print(settings.ROUTE_FACTOR)  # 1.25
print(settings.FUEL_PRICE_PER_LITER)  # 1.50
```

---

## Section 3: Cost Calculations (Brief 03)

### Brief Context

Implement fuel cost calculations with unit conversions (MPG ↔ L/100km, gallons ↔ liters).

### Implementation Steps

**1. Create cost utility module**

File: `apps/calculators/costs.py`:

```python
"""Cost estimation utilities for travel."""
from django.conf import settings

def calculate_fuel_cost(
    distance_km: float,
    fuel_economy_l_per_100km: float | None = None,
    fuel_price_per_liter: float | None = None,
) -> float:
    """Calculate fuel cost for a given distance.
    
    Args:
        distance_km: Distance in kilometers
        fuel_economy_l_per_100km: Fuel consumption (L/100km), uses settings default if None
        fuel_price_per_liter: Fuel price (per liter), uses settings default if None
    
    Returns:
        Total fuel cost in currency units
    """
    economy = fuel_economy_l_per_100km or settings.FUEL_ECONOMY_L_PER_100KM
    price = fuel_price_per_liter or settings.FUEL_PRICE_PER_LITER
    
    liters_consumed = (distance_km / 100) * economy
    return liters_consumed * price

def mpg_to_l_per_100km(mpg: float) -> float:
    """Convert miles per gallon (US) to liters per 100 km."""
    return 235.214583 / mpg

def l_per_100km_to_mpg(l_per_100km: float) -> float:
    """Convert liters per 100 km to miles per gallon (US)."""
    return 235.214583 / l_per_100km

def gallons_to_liters(gallons: float) -> float:
    """Convert US gallons to liters."""
    return gallons * 3.78541

def liters_to_gallons(liters: float) -> float:
    """Convert liters to US gallons."""
    return liters / 3.78541
```

**2. Why these formulas?**

**Fuel Cost Formula:**

```
liters_consumed = (distance_km / 100) × L/100km
total_cost = liters_consumed × price_per_liter
```

**MPG ↔ L/100km Conversion:**

- Magic number 235.214583 = (100 km × 3.78541 L/gal) / (1.60934 km/mi)
- Reciprocal relationship: higher MPG = lower L/100km

### Verification

```bash
# Django shell
>>> from apps.calculators.costs import calculate_fuel_cost, mpg_to_l_per_100km
>>> cost = calculate_fuel_cost(500, fuel_economy_l_per_100km=8.0, fuel_price_per_liter=1.50)
>>> print(f"Cost for 500 km: €{cost:.2f}")
Cost for 500 km: €60.00

>>> print(f"30 MPG = {mpg_to_l_per_100km(30):.2f} L/100km")
30 MPG = 7.84 L/100km
```

---

## Section 4: Forms and Validation (Brief 04)

### Brief Context

Create forms that accept city names, IATA codes, or "lat,lon" coordinates, normalize to coordinates, and validate input ranges.

### Django Concepts: Forms

**From Matt Layman's "Understand Django" (Chapter: Forms):**

> Forms validate user input and clean data. Use `clean_<fieldname>()` methods for individual field validation and `clean()` for cross-field validation. Django's form system prevents many common security issues (like XSS and CSRF).

**From Django Documentation:**

> **Cleaning and Validation:** Django calls `clean_<fieldname>()` for each field, then `clean()` for the whole form. Raise `ValidationError` to signal problems.

### Implementation Steps

**1. Create distance calculator form**

File: `apps/calculators/forms.py`:

```python
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.airports.models import Airport

class DistanceCalculatorForm(forms.Form):
    """Form for distance calculator accepting city, IATA, or coordinates."""
    
    origin = forms.CharField(
        max_length=255,
        help_text="City name, IATA code, or 'lat,lon'"
    )
    destination = forms.CharField(
        max_length=255,
        help_text="City name, IATA code, or 'lat,lon'"
    )
    method = forms.ChoiceField(
        choices=[("haversine", "Haversine"), ("geodesic", "Geodesic")],
        initial=settings.DEFAULT_DISTANCE_METHOD
    )
    unit = forms.ChoiceField(
        choices=[("km", "Kilometers"), ("mi", "Miles")],
        initial=settings.DEFAULT_DISTANCE_UNIT
    )
    include_driving = forms.BooleanField(required=False, initial=True)
    
    def clean_origin(self):
        return self._normalize_location(self.cleaned_data["origin"], "origin")
    
    def clean_destination(self):
        return self._normalize_location(self.cleaned_data["destination"], "destination")
    
    def _normalize_location(self, value: str, field_name: str) -> dict[str, float]:
        """Convert city/IATA/coords to {'lat': ..., 'lon': ...}."""
        value = value.strip()
        
        # Try lat,lon format
        if "," in value:
            try:
                lat_str, lon_str = value.split(",")
                lat = float(lat_str.strip())
                lon = float(lon_str.strip())
                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                    raise ValidationError(f"Coordinates out of range: {value}")
                return {"lat": lat, "lon": lon}
            except (ValueError, ValidationError):
                raise ValidationError(f"Invalid coordinates: {value}")
        
        # Try IATA code lookup
        airport = Airport.objects.filter(iata_code__iexact=value).first()
        if airport:
            return {"lat": airport.latitude_deg, "lon": airport.longitude_deg}
        
        # Try city name lookup (simplified; expand with City model)
        raise ValidationError(f"Could not resolve '{value}' to coordinates. Try IATA code or 'lat,lon'.")

class CostCalculatorForm(DistanceCalculatorForm):
    """Extends distance form with cost parameters."""
    
    fuel_economy = forms.FloatField(
        initial=settings.FUEL_ECONOMY_L_PER_100KM,
        min_value=1.0,
        max_value=50.0,
        help_text="Liters per 100 km"
    )
    fuel_price = forms.FloatField(
        initial=settings.FUEL_PRICE_PER_LITER,
        min_value=0.1,
        max_value=10.0,
        help_text="Price per liter"
    )
```

### Verification

```python
# Django shell
from apps.calculators.forms import DistanceCalculatorForm

form = DistanceCalculatorForm(data={
    "origin": "JFK",
    "destination": "LAX",
    "method": "haversine",
    "unit": "mi",
    "include_driving": True
})

if form.is_valid():
    print(form.cleaned_data["origin"])  # {'lat': 40.6398, 'lon': -73.7789}
    print(form.cleaned_data["destination"])  # {'lat': 33.9425, 'lon': -118.408}
```

---

## Section 5: Views, URLs, and HTMX (Brief 05)

### Brief Context

Create CBVs for distance and cost calculators, wire up URLs, and implement HTMX partial responses.

### Django Concepts: Class-Based Views

**From Matt Layman's "Understand Django" (Chapter: Views):**

> `FormView` is perfect for forms that don't map to a single model. Override `form_valid()` to process cleaned data and return a response. For HTMX, check `request.headers.get("HX-Request")` and return a partial template.

**HTMX Documentation:**

> **HX-Request Header:** HTMX sets this header on all requests. Use it to detect HTMX and return HTML fragments instead of full pages.

### Implementation Steps

**1. Create views**

File: `apps/calculators/views.py`:

```python
from django.views.generic import FormView
from django.shortcuts import render
from .forms import DistanceCalculatorForm, CostCalculatorForm
from .geo import calculate_distance_between_points, estimate_driving_distance
from .costs import calculate_fuel_cost

class DistanceCalculatorView(FormView):
    template_name = "calculators/distance_calculator.html"
    form_class = DistanceCalculatorForm
    
    def form_valid(self, form):
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        method = form.cleaned_data["method"]
        unit = form.cleaned_data["unit"]
        include_driving = form.cleaned_data["include_driving"]
        
        flight_distance = calculate_distance_between_points(
            origin["lat"], origin["lon"],
            destination["lat"], destination["lon"],
            method=method, unit=unit
        )
        
        driving_distance = None
        if include_driving:
            driving_distance = estimate_driving_distance(flight_distance)
        
        context = self.get_context_data(
            form=form,
            flight_distance=flight_distance,
            driving_distance=driving_distance,
            unit=unit
        )
        
        if self.request.headers.get("HX-Request"):
            return render(self.request, "calculators/partials/_distance_results.html", context)
        
        return self.render_to_response(context)

class CostCalculatorView(FormView):
    template_name = "calculators/cost_calculator.html"
    form_class = CostCalculatorForm
    
    def form_valid(self, form):
        origin = form.cleaned_data["origin"]
        destination = form.cleaned_data["destination"]
        method = form.cleaned_data["method"]
        fuel_economy = form.cleaned_data["fuel_economy"]
        fuel_price = form.cleaned_data["fuel_price"]
        
        distance_km = calculate_distance_between_points(
            origin["lat"], origin["lon"],
            destination["lat"], destination["lon"],
            method=method, unit="km"
        )
        
        cost = calculate_fuel_cost(distance_km, fuel_economy, fuel_price)
        
        context = self.get_context_data(
            form=form,
            distance_km=distance_km,
            cost=cost
        )
        
        if self.request.headers.get("HX-Request"):
            return render(self.request, "calculators/partials/_cost_results.html", context)
        
        return self.render_to_response(context)
```

**2. Wire up URLs**

File: `apps/calculators/urls.py`:

```python
from django.urls import path
from .views import DistanceCalculatorView, CostCalculatorView

app_name = "calculators"
urlpatterns = [
    path("distance/", DistanceCalculatorView.as_view(), name="distance"),
    path("cost/", CostCalculatorView.as_view(), name="cost"),
]
```

**3. Create templates**

File: `apps/calculators/templates/calculators/distance_calculator.html`:

```html
{% extends "base.html" %}
{% block content %}
<div class="container mt-4">
  <h1>Distance Calculator</h1>
  
  <form method="post" hx-post="{% url 'calculators:distance' %}" hx-target="#results">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Calculate</button>
  </form>
  
  <div id="results" class="mt-4">
    {% include "calculators/partials/_distance_results.html" %}
  </div>
</div>
{% endblock %}
```

File: `apps/calculators/templates/calculators/partials/_distance_results.html`:

```html
{% if flight_distance %}
<div class="alert alert-success">
  <h4>Results</h4>
  <p><strong>Flight Distance:</strong> {{ flight_distance|floatformat:2 }} {{ unit }}</p>
  {% if driving_distance %}
  <p><strong>Estimated Driving Distance:</strong> {{ driving_distance|floatformat:2 }} {{ unit }}</p>
  {% endif %}
</div>
{% endif %}
```

### Verification

```bash
# Start server
uv run python travelmathlite/manage.py runserver

# Visit: http://localhost:8000/calculators/distance/
# Try: origin="JFK", destination="LAX", method="haversine", unit="mi"
```

---

## Section 6: Algorithm Documentation (Brief 06)

### Brief Context

Document the distance and cost algorithms with formulas, examples, and edge cases.

### Implementation Steps

**1. Create documentation file**

File: `docs/travelmathlite/algorithms/distance-and-cost.md`:

Key sections:

- **Haversine Formula:** Mathematical derivation and constants
- **Geodesic Distance:** When to use and accuracy comparison
- **Route Factor:** Justification for 1.25 default
- **Fuel Cost Formula:** Breakdown with examples
- **Unit Conversions:** MPG ↔ L/100km, km ↔ mi, gallons ↔ liters
- **Edge Cases:** Antipodal points, polar regions, invalid coordinates
- **Performance:** Expected calculation times for various distances

### Verification

- Review documentation for completeness
- Ensure examples match actual implementation
- Run full test suite to validate documented behavior

---

## Summary and Next Steps

You've now implemented complete distance and cost calculators:

1. **Core Algorithms:** Haversine, geodesic, unit conversions, driving estimates
2. **Settings Integration:** Project-wide defaults for route factors and costs
3. **Cost Calculations:** Fuel cost with MPG/L conversions
4. **Forms:** City/IATA/coordinate normalization with validation
5. **Views and HTMX:** Dynamic UI updates with partial responses
6. **Documentation:** Algorithm explanations with formulas and examples

**Next Steps:**

- Add more sophisticated geocoding for city names
- Implement caching for frequently calculated routes
- Add time estimation based on average speed
- Support multi-leg trips with waypoints

## Full References

**Matt Layman's "Understand Django":**

- Chapter: Views (FormView, template rendering)
- Chapter: Forms (validation, cleaning)
- Chapter: Settings (configuration management)
- Chapter: Testing (unit tests for utilities)

**Django Documentation:**

- [Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Settings](https://docs.djangoproject.com/en/stable/topics/settings/)

**Bootstrap Documentation:**

- [Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
- [Alerts](https://getbootstrap.com/docs/5.3/components/alerts/)

**HTMX Documentation:**

- [Attributes](https://htmx.org/attributes/)
- [Request Headers](https://htmx.org/reference/#request_headers)
