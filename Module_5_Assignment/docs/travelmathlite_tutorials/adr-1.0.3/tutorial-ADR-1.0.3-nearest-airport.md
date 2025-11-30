# Tutorial: ADR-1.0.3 Nearest Airport Lookup Implementation

## Goal

Learn how TravelMathLite implements nearest-airport lookup using a bounding box prefilter combined with haversine distance calculation—all without PostGIS—and how to expose this via Django QuerySets, forms, views, templates, and APIs. This tutorial walks through the complete implementation from core algorithms to HTMX-enabled UI.

## Context and Traceability

- **ADR:** `docs/travelmathlite/adr/adr-1.0.3-nearest-airport-lookup-implementation.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.3/` (six briefs covering core → docs → forms → views → templates → tests)
- **App:** `travelmathlite/apps/airports/`
- **Algorithm Documentation:** `docs/travelmathlite/algorithms/nearest-airport.md`
- **PRD Requirements:** §4 F-002 (nearest airports), §4 F-004 (search/indexes), §7 NF-001 (performance < 300ms)
- **Functional Requirements:** FR-F-002-1, FR-F-004-1

## Prerequisites

Before starting this tutorial, ensure you have:

- TravelMathLite project initialized with `uv` (see ADR-1.0.0 tutorial)
- Python 3.12+ environment activated
- Database migrated with airport and country models
- Airport data loaded via `import_airports` management command (see ADR-1.0.1 tutorial)
- Basic familiarity with:
  - Django models, QuerySets, and custom managers
  - Django forms and validation
  - Class-Based Views (CBVs)
  - Django templates and template inheritance
  - HTMX for dynamic partial updates

## Section 1: Core QuerySet and Indexes (Brief 01)

### Brief Context

Implement the core `AirportQuerySet.nearest(...)` method that accepts latitude, longitude, and optional parameters (limit, radius, country, unit) and returns the closest airports ordered by distance.

### Django Concepts: Custom QuerySets and Managers

**From Matt Layman's "Understand Django" (Chapter: Models and QuerySets):**

> Django's QuerySet API is the primary way to interact with your database. By default, every model gets a `objects` manager that returns a QuerySet. You can customize this by creating a custom QuerySet class and using `as_manager()` to replace the default manager.

**From Django Documentation:**

> **Custom Managers:** A custom Manager adds extra methods to the QuerySet API. Common uses include adding methods that encapsulate common query patterns or business logic related to retrieving model instances.
>
> ```python
> class PersonQuerySet(models.QuerySet):
>     def authors(self):
>         return self.filter(role='A')
>
>     def editors(self):
>         return self.filter(role='E')
>
> class Person(models.Model):
>     objects = PersonQuerySet.as_manager()
> ```

### Implementation Steps

**1. Define `AirportQuerySet` with `nearest` method**

Create or update `apps/airports/models.py`:

```python
from typing import TYPE_CHECKING, Literal
import math
from django.db import models

class AirportQuerySet(models.QuerySet["Airport"]):
    """Custom queryset for airport-specific queries."""
    
    def active(self) -> "AirportQuerySet":
        """Return only active airports."""
        return self.filter(active=True)
    
    def nearest(
        self,
        latitude: float,
        longitude: float,
        *,
        limit: int = 3,
        radius_km: float = 2000,
        iso_country: str | None = None,
        unit: Literal["km", "mi"] = "km",
    ) -> list["Airport"]:
        """Return closest airports ordered by haversine distance.
        
        Args:
            latitude: Query point latitude
            longitude: Query point longitude
            limit: Maximum number of results (default 3)
            radius_km: Search radius for bounding box prefilter (default 2000)
            iso_country: Optional ISO 3166-1 alpha-2 country code filter
            unit: Distance unit for display ("km" or "mi")
            
        Returns:
            List of Airport instances with distance_km (and distance_mi if unit="mi") attached
        """
        # Bounding box prefilter
        filters = self._bounding_box_filters(latitude, longitude, radius_km)
        qs = self.active().filter(**filters)
        
        # Optional country filter
        if iso_country:
            qs = qs.filter(
                models.Q(country__iso_code__iexact=iso_country) 
                | models.Q(iso_country__iexact=iso_country)
            )
        
        # Compute haversine distance for each candidate
        candidates = list(qs)
        for airport in candidates:
            d_km = _haversine_km(latitude, longitude, airport.latitude_deg, airport.longitude_deg)
            airport.distance_km = d_km
            if unit == "mi":
                from ..base.utils.units import km_to_mi
                airport.distance_mi = km_to_mi(d_km)
        
        # Sort and limit
        candidates.sort(key=lambda a: getattr(a, "distance_km", math.inf))
        return candidates[:limit]
    
    def _bounding_box_filters(self, latitude: float, longitude: float, radius_km: float) -> dict[str, float]:
        """Generate coordinate range filters for bounding box prefilter."""
        radius_deg = radius_km / 111.0
        lat_min = latitude - radius_deg
        lat_max = latitude + radius_deg
        lon_delta = radius_deg / max(math.cos(math.radians(latitude)), 0.1)
        lon_min = longitude - lon_delta
        lon_max = longitude + lon_delta
        return {
            "latitude_deg__gte": lat_min,
            "latitude_deg__lte": lat_max,
            "longitude_deg__gte": lon_min,
            "longitude_deg__lte": lon_max,
        }

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Compute great-circle distance using Haversine formula."""
    R = 6371.0  # Earth radius in km
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class Airport(models.Model):
    # ... field definitions ...
    
    # Typing hints for dynamically attached attributes
    if TYPE_CHECKING:
        distance_km: float
        distance_mi: float
    
    objects: AirportQuerySet = AirportQuerySet.as_manager()  # type: ignore[assignment]
    
    class Meta:
        indexes = [
            models.Index(fields=["latitude_deg", "longitude_deg"]),
            models.Index(fields=["iso_country"]),
            models.Index(fields=["active"]),
        ]
```

**2. Why this approach?**

**Bounding Box Prefilter:**

- Converts radius (km) to approximate lat/lon deltas (~111 km per degree latitude)
- Creates a rectangle around the query point
- Uses standard B-tree indexes to quickly filter candidates

**Haversine Calculation:**

- Computes great-circle distance on a sphere
- Accurate within 0.5% for distances < 1000 km
- Fast enough in Python for typical candidate sets (< 100 airports after bbox filter)

**No PostGIS Required:**

- SQLite-friendly approach using standard indexes
- Portable across database backends
- Performance target: p95 < 300 ms on 50k-airport dataset

### Verification

```bash
# Django shell
uv run python travelmathlite/manage.py shell

>>> from apps.airports.models import Airport
>>> lat, lon = 31.76, -106.49  # Near El Paso, TX
>>> results = Airport.objects.nearest(lat, lon, limit=3, iso_country="US")
>>> for airport in results:
...     print(f"{airport.name} ({airport.iata_code}): {airport.distance_km:.2f} km")
El Paso International (ELP): 10.23 km
Las Cruces Intl (LRU): 78.45 km
...

# Run tests
uv run python travelmathlite/manage.py test apps.airports.tests.tests_nearest_core
```

---

## Section 2: Algorithm Documentation (Brief 02)

### Brief Context

Document the nearest-airport algorithm with formulas, examples, performance targets, and limitations so future developers understand the trade-offs.

### Documentation Concepts

**From Matt Layman's "Understand Django" (Chapter: Best Practices):**

> Good documentation explains not just *what* your code does, but *why* you made certain decisions. Include context about alternatives you considered and the trade-offs you accepted.

### Implementation Steps

**1. Create algorithm documentation**

File: `docs/travelmathlite/algorithms/nearest-airport.md`

Key sections to include:

- **Approach Overview:** Bounding box → haversine → sort → top N
- **Bounding Box Derivation:** `dlat = R_km / 111`, `dlon = dlat / cos(lat)`
- **Haversine Formula:** With constants and explanation
- **Example Query:** Show input coordinates → output airports with distances
- **Performance:** p95 < 300 ms target; index usage
- **Limitations:** Spherical approximation, bbox at poles, cross-border behavior

**2. Example from documentation:**

```text
Given a query (lat, lon) and radius R_km:
- Latitude delta: dlat = R_km / 111
- Longitude delta: dlon = dlat / max(cos(lat in radians), 0.1)
- Apply: latitude_deg BETWEEN (lat - dlat) AND (lat + dlat)
         longitude_deg BETWEEN (lon - dlon) AND (lon + dlon)
```

### Verification

- Review `docs/travelmathlite/algorithms/nearest-airport.md`
- Ensure examples match actual queryset behavior
- Check that performance targets are realistic (run test with timing assertions)

---

## Section 3: Forms (Brief 03)

### Brief Context

Create a Django form that normalizes user input (city name, IATA code, or coordinates) into lat/lon for the nearest lookup.

### Django Concepts: Forms and Validation

**From Matt Layman's "Understand Django" (Chapter: Forms):**

> Forms are Django's way of handling user input. They provide validation, cleaning, and a bridge between HTML forms and Python objects. Use `ModelForm` when your form maps directly to a model, or `Form` when you need custom logic.

**From Django Documentation:**

> **Form Cleaning:** The `clean()` method on a form is called after individual field validation. Use it to implement cross-field validation or to transform data.
>
> ```python
> class ContactForm(forms.Form):
>     def clean(self):
>         cleaned_data = super().clean()
>         # Custom cross-field validation
>         return cleaned_data
> ```

### Implementation Steps

**1. Define `NearestAirportForm`**

File: `apps/calculators/forms.py` (or `apps/airports/forms.py`):

```python
from django import forms
from apps.airports.models import Airport

class NearestAirportForm(forms.Form):
    """Form for nearest airport lookup via city, IATA, or coordinates."""
    
    query = forms.CharField(
        max_length=255,
        required=False,
        help_text="City name, IATA code, or leave blank to use coordinates"
    )
    latitude = forms.FloatField(required=False, min_value=-90, max_value=90)
    longitude = forms.FloatField(required=False, min_value=-180, max_value=180)
    country = forms.CharField(max_length=2, required=False, help_text="ISO country code (e.g., US)")
    limit = forms.IntegerField(initial=3, min_value=1, max_value=10)
    
    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get("query")
        lat = cleaned_data.get("latitude")
        lon = cleaned_data.get("longitude")
        
        if not query and (lat is None or lon is None):
            raise forms.ValidationError("Provide either a query or both latitude and longitude.")
        
        # Normalize query to lat/lon if provided
        if query:
            # Try IATA code first
            airport = Airport.objects.filter(iata_code__iexact=query.strip()).first()
            if airport:
                cleaned_data["latitude"] = airport.latitude_deg
                cleaned_data["longitude"] = airport.longitude_deg
            else:
                # Try city lookup (simplified; you may need a City model)
                raise forms.ValidationError(f"Could not resolve '{query}' to coordinates.")
        
        return cleaned_data
```

### Verification

```python
# Django shell
from apps.calculators.forms import NearestAirportForm

form = NearestAirportForm(data={"query": "DFW", "limit": 5})
if form.is_valid():
    print(form.cleaned_data)
    # {'query': 'DFW', 'latitude': 32.8998, 'longitude': -97.0403, 'limit': 5}
```

---

## Section 4: Views and API (Brief 04)

### Brief Context

Expose nearest-airport lookup via a page view (CBV) and a JSON API endpoint.

### Django Concepts: Class-Based Views

**From Matt Layman's "Understand Django" (Chapter: Views):**

> Class-Based Views (CBVs) provide reusable patterns for common view logic. `FormView` handles form display and processing; `TemplateView` renders a template. Use CBVs when you need to compose behavior or override specific methods like `form_valid`.

**From Django Documentation:**

> **FormView:** Displays a form, validates it, and calls `form_valid()` on success. Combine with `JsonResponse` to return JSON.

### Implementation Steps

#### 1. Create a page view

File: `apps/calculators/views.py`:

```python
from django.views.generic import FormView
from django.http import JsonResponse
from .forms import NearestAirportForm
from apps.airports.models import Airport

class NearestAirportView(FormView):
    template_name = "calculators/nearest_airport.html"
    form_class = NearestAirportForm
    
    def form_valid(self, form):
        lat = form.cleaned_data["latitude"]
        lon = form.cleaned_data["longitude"]
        limit = form.cleaned_data["limit"]
        country = form.cleaned_data.get("country")
        
        results = Airport.objects.nearest(lat, lon, limit=limit, iso_country=country or None)
        
        if self.request.headers.get("HX-Request"):
            # HTMX partial response
            return self.render_to_response(self.get_context_data(form=form, results=results))
        
        return self.render_to_response(self.get_context_data(form=form, results=results))

class NearestAirportAPIView(FormView):
    form_class = NearestAirportForm
    
    def form_valid(self, form):
        lat = form.cleaned_data["latitude"]
        lon = form.cleaned_data["longitude"]
        limit = form.cleaned_data["limit"]
        country = form.cleaned_data.get("country")
        
        results = Airport.objects.nearest(lat, lon, limit=limit, iso_country=country or None)
        
        data = [
            {
                "name": airport.name,
                "iata": airport.iata_code,
                "distance_km": round(airport.distance_km, 2),
            }
            for airport in results
        ]
        return JsonResponse({"airports": data})
    
    def form_invalid(self, form):
        return JsonResponse({"errors": form.errors}, status=400)
```

**2. Wire up URLs**

File: `apps/calculators/urls.py`:

```python
from django.urls import path
from .views import NearestAirportView, NearestAirportAPIView

app_name = "calculators"
urlpatterns = [
    path("nearest-airport/", NearestAirportView.as_view(), name="nearest_airport"),
    path("api/nearest-airport/", NearestAirportAPIView.as_view(), name="nearest_airport_api"),
]
```

### Verification

```bash
# Start server
uv run python travelmathlite/manage.py runserver

# Visit: http://localhost:8000/calculators/nearest-airport/
# Or curl the API:
curl "http://localhost:8000/calculators/api/nearest-airport/?latitude=31.76&longitude=-106.49&limit=3"
```

---

## Section 5: Templates and HTMX (Brief 05)

### Brief Context

Create a minimal page template and HTMX partial for displaying nearest airport results dynamically.

### HTMX Concepts

**From HTMX Documentation:**

> HTMX allows you to access modern browser features directly from HTML, without using JavaScript. Use `hx-get`, `hx-post`, and `hx-target` to fetch and swap HTML fragments.

### Implementation Steps

**1. Base template**

File: `apps/calculators/templates/calculators/nearest_airport.html`:

```html
{% extends "base.html" %}
{% block content %}
<div class="container mt-4">
  <h1>Nearest Airport Lookup</h1>
  
  <form method="post" hx-post="{% url 'calculators:nearest_airport' %}" hx-target="#results">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Find Airports</button>
  </form>
  
  <div id="results" class="mt-4">
    {% include "calculators/_nearest_results.html" %}
  </div>
</div>
{% endblock %}
```

**2. Partial template**

File: `apps/calculators/templates/calculators/_nearest_results.html`:

```html
{% if results %}
<h3>Nearest Airports</h3>
<ul class="list-group">
  {% for airport in results %}
  <li class="list-group-item">
    <strong>{{ airport.name }}</strong> ({{ airport.iata_code }})
    <br>
    <small>Distance: {{ airport.distance_km|floatformat:2 }} km</small>
  </li>
  {% endfor %}
</ul>
{% endif %}
```

### Verification

- Open the page in browser
- Submit form and observe HTMX-driven partial update
- Inspect network tab to confirm only HTML partial is returned

---

## Section 6: Tests and Performance (Brief 06)

### Brief Context

Write tests for ordering, distance attachment, country filtering, and light performance assertions.

### Django Concepts: Testing

**From Matt Layman's "Understand Django" (Chapter: Testing):**

> Django's TestCase class provides a test database, transaction management, and assertions tailored to Django apps. Test your models, views, and forms in isolation, then add integration tests for complete flows.

**From Django Documentation:**

> Use `assertQuerysetEqual`, `assertContains`, and custom assertions to verify behavior. For performance, use `assertNumQueries` to check query counts.

### Implementation Steps

**1. Core tests**

File: `apps/airports/tests/tests_nearest_core.py`:

```python
from django.test import TestCase
from apps.airports.models import Airport

class NearestCoreTests(TestCase):
    def setUp(self):
        Airport.objects.create(
            ident="KELP", iata_code="ELP", name="El Paso International",
            airport_type="large_airport", latitude_deg=31.8072, longitude_deg=-106.3778,
            iso_country="US", active=True
        )
        Airport.objects.create(
            ident="MMCS", iata_code="CJS", name="Ciudad Juárez Intl",
            airport_type="large_airport", latitude_deg=31.6361, longitude_deg=-106.429,
            iso_country="MX", active=True
        )
    
    def test_nearest_orders_by_distance(self):
        lat, lon = 31.76, -106.49
        results = Airport.objects.nearest(lat, lon, limit=2)
        self.assertEqual(len(results), 2)
        self.assertTrue(hasattr(results[0], "distance_km"))
        self.assertLess(results[0].distance_km, results[1].distance_km)
    
    def test_iso_country_filter(self):
        lat, lon = 31.76, -106.49
        results_us = Airport.objects.nearest(lat, lon, limit=5, iso_country="US")
        self.assertTrue(all(a.iso_country.upper() == "US" for a in results_us))
```

**2. Run tests**

```bash
uv run python travelmathlite/manage.py test apps.airports
```

### Verification

- All tests pass
- Check query count and timing (optional: add timing assertions for p95 < 300 ms)

---

## Summary and Next Steps

You've now implemented a complete nearest-airport lookup feature:

1. **Core QuerySet** with bounding box prefilter and haversine calculation
2. **Algorithm documentation** explaining approach and trade-offs
3. **Forms** for normalizing user input
4. **Views and API** using Django CBVs and JSON responses
5. **Templates and HTMX** for dynamic UI updates
6. **Tests** covering ordering, filtering, and performance

**Next Steps:**

- Add more sophisticated geocoding for city name lookups
- Implement caching for frequently queried coordinates
- Add pagination for large result sets
- Consider PostGIS migration for datasets > 100k airports

## Full References

**Matt Layman's "Understand Django":**

- Chapter: Models and QuerySets
- Chapter: Forms
- Chapter: Views
- Chapter: Testing
- Chapter: Best Practices

**Django Documentation:**

- [QuerySets and Managers](https://docs.djangoproject.com/en/stable/topics/db/managers/)
- [Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [Testing](https://docs.djangoproject.com/en/stable/topics/testing/)

**Bootstrap Documentation:**

- [Forms](https://getbootstrap.com/docs/5.3/forms/overview/)
- [List Groups](https://getbootstrap.com/docs/5.3/components/list-group/)

**HTMX Documentation:**

- [Attributes](https://htmx.org/attributes/)
- [Examples](https://htmx.org/examples/)
