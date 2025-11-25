# Tutorial: ADR-1.0.0 Application Architecture & App Boundaries

## Goal

Learn how TravelMathLite organizes functionality into Django apps with clear boundaries, namespaced URLs, shared templates, and a scalable project structure that supports feature growth.

## Context

- **ADR:** `docs/travelmathlite/adr/adr-1.0.0-application-architecture-and-app-boundaries.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.0/` (six briefs covering scaffolding → settings → URLs → templates → tests → docs)
- **Apps:** `travelmathlite/apps/*` (calculators, airports, accounts, trips, search, base)
- **Architecture Documentation:** `docs/travelmathlite/architecture/app-layout.md`

## Prerequisites

- TravelMathLite project initialized with `uv`
- Python environment activated
- Basic familiarity with Django project structure

## Section 1: Django Apps and Boundaries (Brief 01)

### Brief Context

Design a multi-app architecture with clear domain boundaries to support feature modularity, team collaboration, and future scaling.

### Django Concepts: Apps and Project Structure

**From Matt Layman's "Understand Django" (Chapter: Project Structure):**

> Django projects are composed of apps. Each app should represent a distinct area of functionality—think of them as mini-applications within your project. Good app boundaries make code easier to understand, test, and reuse. A project should have:
>
> - One core configuration package (`core/` or `config/`)
> - Multiple domain apps with focused responsibilities
> - Shared utilities in a `base` or `common` app

**From Django Documentation:**

> **What is an app?** An app is a Python package that contains models, views, templates, and other code. Apps should be self-contained and reusable. Use `startapp` to create the basic structure, then organize apps under a top-level `apps/` directory for clarity.

### TravelMathLite App Boundaries

**Domain Apps:**

- **`base`**: Shared models (Country, City), utilities, base templates
- **`calculators`**: Distance, cost, time calculators; forms and views
- **`airports`**: Airport search, nearest-airport lookup, data import
- **`accounts`**: User auth, profiles, preferences
- **`trips`**: Trip planning, itineraries, saved routes
- **`search`**: Global search across airports, cities, trips

**Core Configuration:**

- **`core`**: Settings, root URLs, WSGI/ASGI config (no models/views)

### Implementation Steps

**1. Create app structure**

```bash
# Using Django's startapp inside apps/ directory
cd travelmathlite
mkdir -p apps
cd apps

uv run python ../manage.py startapp base
uv run python ../manage.py startapp calculators
uv run python ../manage.py startapp airports
uv run python ../manage.py startapp accounts
uv run python ../manage.py startapp trips
uv run python ../manage.py startapp search
```

**2. Configure each app**

File: `apps/calculators/apps.py`:

```python
from django.apps import AppConfig

class CalculatorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.calculators'
    verbose_name = 'Distance & Cost Calculators'
```

**3. Define app-level URLs**

File: `apps/calculators/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('distance/', views.DistanceCalculatorView.as_view(), name='distance'),
    path('cost/', views.CostCalculatorView.as_view(), name='cost'),
]
```

**4. Create app templates directory**

```
apps/calculators/
  templates/
    calculators/
      index.html
      distance_calculator.html
      cost_calculator.html
      partials/
        _distance_results.html
```

### Why This Structure?

**Benefits:**

- **Clear Ownership:** Each app owns its domain (calculators vs. airports vs. trips)
- **Team Scalability:** Multiple developers can work on different apps without conflicts
- **Reusability:** Apps can be extracted or shared across projects
- **Testing:** Test each app in isolation with focused test suites
- **URL Namespacing:** Avoid name collisions (`calculators:index` vs. `airports:index`)

**Trade-offs:**

- **Overhead:** More files and directories to manage
- **Cross-App Dependencies:** Manage carefully (use imports sparingly; prefer events/signals)

### Verification

```bash
# Check app structure
ls -la travelmathlite/apps/
# Should show: base/ calculators/ airports/ accounts/ trips/ search/

# Verify apps.py configuration
uv run python travelmathlite/manage.py shell
>>> from django.apps import apps
>>> print([app.name for app in apps.get_app_configs() if app.name.startswith('apps.')])
['apps.base', 'apps.calculators', 'apps.airports', 'apps.accounts', 'apps.trips', 'apps.search']
```

---

## Section 2: Settings and Installed Apps (Brief 02)

### Brief Context

Register all domain apps in `INSTALLED_APPS`, configure template directories, and organize settings for development/production.

### Django Concepts: Settings Management

**From Matt Layman's "Understand Django" (Chapter: Settings):**

> Django's settings module is the heart of your configuration. For larger projects, split settings into `base.py`, `dev.py`, and `prod.py`. Use environment variables for secrets. Always list your apps in `INSTALLED_APPS` so Django can discover models, templates, and management commands.

**From Django Documentation:**

> **INSTALLED_APPS:** Django needs to know about your apps to register models, run migrations, and collect static files. List apps in dependency order (Django's built-ins first, third-party next, then your apps).

### Implementation Steps

**1. Configure INSTALLED_APPS**

File: `core/settings.py`:

```python
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps (if any)
    # 'django_extensions',
    
    # TravelMathLite apps (domain order: base first, then features)
    'apps.base.apps.BaseConfig',
    'apps.calculators.apps.CalculatorsConfig',
    'apps.airports.apps.AirportsConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.trips.apps.TripsConfig',
    'apps.search.apps.SearchConfig',
]
```

**2. Configure templates**

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Project-level templates (base.html)
        ],
        'APP_DIRS': True,  # Enable per-app templates/ discovery
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**3. Static files configuration**

```python
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Project-level static files
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Collected static files for production
```

### Template Resolution Order

Django searches for templates in this order:

1. `TEMPLATES['DIRS']` (project-level `templates/`)
2. App-specific `templates/` directories (if `APP_DIRS=True`)

**Example:** For `{% extends "base.html" %}`:

- Checks `travelmathlite/templates/base.html` (found ✓)

**Example:** For `{% include "calculators/distance_calculator.html" %}`:

- Checks `travelmathlite/templates/calculators/distance_calculator.html` (not found)
- Checks `apps/calculators/templates/calculators/distance_calculator.html` (found ✓)

### Verification

```python
# Django shell
uv run python travelmathlite/manage.py shell

>>> from django.conf import settings
>>> print(settings.INSTALLED_APPS)
>>> print(settings.TEMPLATES[0]['DIRS'])

# Run checks
uv run python travelmathlite/manage.py check
```

---

## Section 3: URL Configuration and Namespacing (Brief 03)

### Brief Context

Create a root URL configuration that includes each app's URLs with namespacing to avoid name collisions.

### Django Concepts: URL Routing

**From Matt Layman's "Understand Django" (Chapter: URLs and Routing):**

> URLs are the entry point to your views. Use `include()` to delegate URL patterns to apps, keeping your root URLconf clean. Use `app_name` in each app's `urls.py` to create namespaces. Reverse URLs with `reverse('app_name:view_name')` or `{% url 'app_name:view_name' %}` in templates.

**From Django Documentation:**

> **URL Namespacing:** Use `app_name` in your app's `urls.py` to namespace URLs. This prevents collisions when multiple apps have views with the same name. Reference namespaced URLs with `reverse('namespace:name')`.

### Implementation Steps

**1. Create root URL configuration**

File: `core/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App URLs (namespaced)
    path('', include('apps.base.urls')),  # Homepage, about, etc.
    path('calculators/', include('apps.calculators.urls')),
    path('airports/', include('apps.airports.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('trips/', include('apps.trips.urls')),
    path('search/', include('apps.search.urls')),
]
```

**2. Define app URL namespaces**

File: `apps/calculators/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'calculators'  # Namespace

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('distance/', views.DistanceCalculatorView.as_view(), name='distance'),
    path('cost/', views.CostCalculatorView.as_view(), name='cost'),
]
```

File: `apps/airports/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'airports'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('<str:iata_code>/', views.DetailView.as_view(), name='detail'),
    path('api/nearest/', views.NearestAPIView.as_view(), name='nearest_api'),
]
```

**3. Use namespaced URLs in templates**

File: `templates/base.html`:

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container">
    <a class="navbar-brand" href="{% url 'base:home' %}">TravelMathLite</a>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="{% url 'calculators:index' %}">Calculators</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{% url 'airports:index' %}">Airports</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="{% url 'trips:index' %}">Trips</a>
      </li>
    </ul>
  </div>
</nav>
```

### Verification

```bash
# Test URL reversing
uv run python travelmathlite/manage.py shell

>>> from django.urls import reverse
>>> reverse('calculators:index')
'/calculators/'
>>> reverse('calculators:distance')
'/calculators/distance/'
>>> reverse('airports:detail', args=['JFK'])
'/airports/JFK/'

# Test in browser
uv run python travelmathlite/manage.py runserver
# Visit: http://localhost:8000/calculators/
```

---

## Section 4: Template Organization and Inheritance (Brief 04)

### Brief Context

Create a base template layout with Bootstrap/HTMX, then extend it in app-specific templates to maintain consistent UI.

### Django Concepts: Template Inheritance

**From Matt Layman's "Understand Django" (Chapter: Templates):**

> Django templates support inheritance via `{% extends "base.html" %}` and `{% block content %}`. Define a base layout with common elements (navbar, footer) once, then override blocks in child templates. This keeps your UI consistent and reduces duplication.

**Bootstrap Integration:**

Use Bootstrap for responsive layout, forms, and components. Include via CDN or local static files.

**HTMX Integration:**

Add HTMX for dynamic partial updates without full page reloads. Use `hx-get`, `hx-post`, and `hx-target` attributes.

### Implementation Steps

**1. Create base template**

File: `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}TravelMathLite{% endblock %}</title>
  
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  
  <!-- HTMX -->
  <script src="https://unpkg.com/htmx.org@1.9.10"></script>
  
  {% block extra_head %}{% endblock %}
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container">
      <a class="navbar-brand" href="{% url 'base:home' %}">TravelMathLite</a>
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="{% url 'calculators:index' %}">Calculators</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{% url 'airports:index' %}">Airports</a>
        </li>
      </ul>
    </div>
  </nav>
  
  <main class="container mt-4">
    {% block content %}{% endblock %}
  </main>
  
  <footer class="mt-5 py-3 bg-light">
    <div class="container text-center">
      <small>Airport data from OurAirports.com</small>
    </div>
  </footer>
  
  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>
```

**2. Create app-specific template**

File: `apps/calculators/templates/calculators/index.html`:

```html
{% extends "base.html" %}

{% block title %}Calculators - TravelMathLite{% endblock %}

{% block content %}
<h1>Travel Calculators</h1>
<p>Choose a calculator:</p>

<div class="row">
  <div class="col-md-6">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Distance Calculator</h5>
        <p class="card-text">Calculate flight and driving distances between airports or cities.</p>
        <a href="{% url 'calculators:distance' %}" class="btn btn-primary">Open</a>
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Cost Calculator</h5>
        <p class="card-text">Estimate fuel costs based on distance and consumption.</p>
        <a href="{% url 'calculators:cost' %}" class="btn btn-primary">Open</a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

**3. Create HTMX partial template**

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

### Template Organization Best Practices

**Directory Structure:**

```
templates/                  # Project-level
  base.html
  404.html
  500.html

apps/calculators/templates/calculators/   # App-level (note: calculators/ subfolder)
  index.html
  distance_calculator.html
  partials/
    _distance_results.html
```

**Why the double `calculators/` folder?**

Django searches all app `templates/` directories. Without the subfolder, `index.html` from different apps would collide. The subfolder acts as a namespace.

### Verification

```bash
# Start server and visit pages
uv run python travelmathlite/manage.py runserver

# Visit:
# http://localhost:8000/calculators/
# http://localhost:8000/airports/

# Check template inheritance (view source, look for base.html elements)
```

---

## Section 5: Tests for Architecture (Brief 05)

### Brief Context

Write tests to verify URL reversing, template rendering, and app isolation.

### Implementation Steps

**1. Create architecture tests**

File: `apps/base/tests/test_architecture.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse, resolve

class ArchitectureTests(TestCase):
    def test_url_namespacing(self):
        """Verify all app URLs are namespaced and reversible."""
        urls_to_test = [
            ('calculators:index', '/calculators/'),
            ('calculators:distance', '/calculators/distance/'),
            ('airports:index', '/airports/'),
        ]
        
        for name, expected_path in urls_to_test:
            with self.subTest(name=name):
                path = reverse(name)
                self.assertEqual(path, expected_path)
    
    def test_template_inheritance(self):
        """Verify app templates extend base.html."""
        client = Client()
        response = client.get(reverse('calculators:index'))
        self.assertEqual(response.status_code, 200)
        
        # Check for base template elements
        self.assertContains(response, '<nav class="navbar')
        self.assertContains(response, 'TravelMathLite')
    
    def test_app_isolation(self):
        """Verify apps don't have circular imports."""
        # Import all apps to check for import errors
        from apps.base import models as base_models
        from apps.calculators import views as calc_views
        from apps.airports import models as airport_models
        
        # No assertions needed—if imports fail, test fails
        self.assertTrue(True)
```

### Verification

```bash
uv run python travelmathlite/manage.py test apps.base.tests.test_architecture
```

---

## Section 6: Architecture Documentation (Brief 06)

### Brief Context

Document the app boundaries, responsibilities, and dependency rules for future developers.

### Implementation Steps

**1. Create architecture documentation**

File: `docs/travelmathlite/architecture/app-layout.md`:

```markdown
# TravelMathLite App Architecture

## App Boundaries and Responsibilities

### `apps.base`
**Purpose:** Shared models, utilities, base templates  
**Owns:** Country, City, currency/unit conversions  
**Dependencies:** None (foundation layer)

### `apps.calculators`
**Purpose:** Distance, cost, time calculators  
**Owns:** Forms, views, algorithms for calculations  
**Dependencies:** `base` (for Country/City lookups)

### `apps.airports`
**Purpose:** Airport data, search, nearest-airport lookup  
**Owns:** Airport model, import commands, search views  
**Dependencies:** `base` (for Country/City foreign keys)

### `apps.accounts`
**Purpose:** User authentication, profiles, preferences  
**Owns:** User model extensions, auth views  
**Dependencies:** `base`

### `apps.trips`
**Purpose:** Trip planning, itineraries, saved routes  
**Owns:** Trip model, itinerary builder, multi-leg calculations  
**Dependencies:** `calculators`, `airports`, `accounts`

### `apps.search`
**Purpose:** Global search across airports, cities, trips  
**Owns:** Search views, indexing, autocomplete  
**Dependencies:** `airports`, `trips`

## Dependency Rules

1. **No Circular Dependencies:** Apps must not import from each other in a cycle
2. **Foundation First:** `base` has no dependencies on other apps
3. **Domain Isolation:** `calculators` and `airports` are independent
4. **Feature Composition:** `trips` and `search` can depend on domain apps
5. **Use Events/Signals:** For loose coupling between apps

## URL Structure

- `/` → `apps.base` (homepage)
- `/calculators/` → `apps.calculators`
- `/airports/` → `apps.airports`
- `/accounts/` → `apps.accounts`
- `/trips/` → `apps.trips`
- `/search/` → `apps.search`

## Testing Strategy

- Each app has its own test suite
- Run app tests in isolation: `python manage.py test apps.calculators`
- Integration tests live in `apps.base.tests.test_integration`
```

### Verification

- Review documentation for clarity
- Ensure all developers can understand app boundaries
- Update as architecture evolves

---

## Summary and Next Steps

You've now established a scalable Django architecture:

1. **App Scaffolding:** Six domain apps with clear boundaries
2. **Settings Management:** All apps registered, templates configured
3. **URL Namespacing:** Namespaced URLs prevent collisions, enable clean reversing
4. **Template Organization:** Base template with inheritance, app-specific overrides
5. **Architecture Tests:** Verify URL reversing, template rendering, app isolation
6. **Documentation:** Architecture decisions documented for team onboarding

**Next Steps:**

- Add API app for REST endpoints (Django REST Framework)
- Implement shared utilities (logging, error handling) in `base`
- Add CI/CD configuration for automated testing
- Consider event-driven architecture with Django signals for loose coupling

## Full References

**Matt Layman's "Understand Django":**

- Chapter: Project Structure (apps, settings, URLs)
- Chapter: Templates (inheritance, template tags)
- Chapter: Testing (TestCase, Client)

**Django Documentation:**

- [Applications](https://docs.djangoproject.com/en/stable/ref/applications/)
- [URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Template Language](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Settings](https://docs.djangoproject.com/en/stable/topics/settings/)

**Bootstrap Documentation:**

- [Layout](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Components](https://getbootstrap.com/docs/5.3/components/)

**HTMX Documentation:**

- [Introduction](https://htmx.org/docs/)
- [Attributes Reference](https://htmx.org/reference/)
