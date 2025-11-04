# travelmathlite — App layout guide (ADR-1.0.0)

This guide documents how the Django project is organized so contributors can navigate quickly and keep changes consistent with ADR-1.0.0.

## Project overview

- Project package: `travelmathlite/core` (settings, urls, wsgi/asgi)
- Domain apps package: `travelmathlite/apps/*`
- Shared templates: `travelmathlite/templates/`
- Tests: colocated per app under each app package

## Directory structure (key paths)

```text
travelmathlite/
  core/
    settings.py
    urls.py
  apps/
    base/
      apps.py
      urls.py
      views.py
      templates/
        base/
          index.html
          partials/_welcome.html
      tests/
        test_base.py
        test_namespaces.py
    calculators/
      apps.py
      urls.py
      views.py
      templates/calculators/index.html
      templates/calculators/partials/_welcome.html
      tests.py
    airports/
      ... (same pattern)
    accounts/
      ... (same pattern)
    trips/
      ... (same pattern)
    search/
      ... (same pattern)
  templates/
    base.html   # global layout used by all app templates
```

Notes

- The internal app previously named `core` was renamed to `base` to avoid confusion with the project package `core`.
- Global layout `templates/base.html` is extended by each app's `index.html`.
- App-specific includes live under `templates/<app>/partials/`.

## URL namespacing

Each app defines a namespaced URLconf and an index route. The project `core/urls.py` includes each with a namespace.

Example: `apps/calculators/urls.py`

```python
from django.urls import path
from .views import IndexView

app_name = "calculators"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]
```

Project include (`travelmathlite/core/urls.py`):

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.base.urls", namespace="base")),
    path("calculators/", include("apps.calculators.urls", namespace="calculators")),
    path("airports/", include("apps.airports.urls", namespace="airports")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("trips/", include("apps.trips.urls", namespace="trips")),
    path("search/", include("apps.search.urls", namespace="search")),
]
```

Reverse examples:

```python
from django.urls import reverse

reverse("base:index")          # "/"
reverse("calculators:index")   # "/calculators/"
reverse("airports:index")      # "/airports/"
reverse("accounts:index")      # "/accounts/"
reverse("trips:index")         # "/trips/"
reverse("search:index")        # "/search/"
```

## Templates

- Shared base layout: `travelmathlite/templates/base.html`
- Per-app templates: `travelmathlite/apps/<app>/templates/<app>/index.html`
- Per-app partials: `travelmathlite/apps/<app>/templates/<app>/partials/_welcome.html`

Example (per-app `index.html`):

```django
{% extends 'base.html' %}
{% block title %}Calculators — travelmathlite{% endblock %}
{% block content %}
  <h1>Calculators</h1>
  {% include 'calculators/partials/_welcome.html' %}
{% endblock %}
```

## Tests

Basic invariants are covered with Django TestCase:

- `reverse('<namespace>:index')` resolves to expected path
- `index.html` renders, extends `base.html`, and includes the app partial

Run tests (from the project directory):

```bash
uv run python manage.py test -v 2
```

## Contribution tips

- Keep PRs small (<300 LOC changed). Use conventional commits.
- Reference the related Issue with `Refs #<num>` (and mirror the commit message as an Issue comment).
- Use `uvx ruff format .` and `uvx ruff check --fix .` to keep lint/format clean.
- Follow the patterns above for new apps: URL namespace, `IndexView`, app-scoped templates, and tests.
