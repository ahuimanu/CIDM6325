# Tutorial: ADR-1.0.4 Search Strategy and URL Design Implementation

## Goal

Learn how TravelMathLite implements comprehensive search functionality with pagination, query highlighting, canonical URLs, and SEO optimization. This tutorial walks through building a production-ready search feature using Django's QuerySet API, template filters, Bootstrap 5 components, and modern web best practices—all while maintaining SQLite compatibility for development environments.

## Context and Traceability

- **ADR:** `docs/travelmathlite/adr/adr-1.0.4-search-strategy-and-url-design.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.4/` (six briefs covering search → pagination → highlighting → URLs → templates → tests)
- **App:** `travelmathlite/apps/search/`
- **PRD Requirements:** §4 F-008 (search with pagination), §4 F-007 (templates and navbar), §10 Acceptance (canonical URLs, sitemap)
- **Functional Requirements:** FR-F-008-1, FR-F-007-1
- **Non-Functional Requirements:** NF-003 (security: template autoescape, safe highlighting)

## Prerequisites

Before starting this tutorial, ensure you have:

- TravelMathLite project initialized with `uv` (see ADR-1.0.0 tutorial)
- Python 3.12+ environment activated
- Database migrated with airport, city, and country models
- Airport data loaded via `import_airports` management command (see ADR-1.0.1 tutorial)
- Bootstrap 5.3.3 included in base template
- Basic familiarity with:
  - Django models, QuerySets, and filtering
  - Django pagination (`Paginator`, `Page`)
  - Class-Based Views (TemplateView)
  - Django template filters and custom template tags
  - Django URL routing and namespacing
  - Bootstrap 5 navbar and pagination components
  - SEO basics (canonical links, sitemaps, robots.txt)

## Section 1: Search View and Query Parsing (Brief 01)

### Brief Context

Implement basic airport/city search view with safe query parsing. Parse `q` from GET parameters, validate non-empty input, perform case-insensitive `icontains` filtering against airport and city fields, and return results suitable for pagination.

### Django Concepts: TemplateView and QuerySet Filtering

**From Matt Layman's "Understand Django" (Chapter: Views):**

> Django's generic Class-Based Views provide reusable patterns for common tasks. `TemplateView` is perfect for pages that primarily render templates with some context data. Override `get_context_data()` to add your custom logic.

**From Django Documentation:**

> **QuerySet Filtering:** The `filter()` method returns a new QuerySet containing objects that match the given lookup parameters. Common lookups include `icontains` (case-insensitive containment) and `iexact` (case-insensitive exact match).
>
> ```python
> # Case-insensitive search
> Entry.objects.filter(headline__icontains='Lennon')
> 
> # Combine multiple filters with Q objects
> from django.db.models import Q
> Entry.objects.filter(Q(headline__icontains='Lennon') | Q(body__icontains='Lennon'))
> ```

**Security Note from Django Documentation:**

> User input from GET/POST parameters should always be validated and sanitized. Django's ORM provides protection against SQL injection when using QuerySet methods, but you must still validate business logic (e.g., empty strings, length limits).

### Implementation Steps

**1. Create the Search App Structure**

```bash
# From project root
cd travelmathlite
uv run python manage.py startapp search apps/search
```

**2. Define SearchView with Query Parsing**

File: `apps/search/views.py`:

```python
from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from django.views.generic import TemplateView

from ..airports.models import Airport
from ..base.models import City


class SearchView(TemplateView):
    """Render search results for airports and cities based on `q`.
    
    Combines results from both Airport and City models using case-insensitive
    icontains filtering. Empty queries return no results without hitting the DB.
    """

    template_name: str = "search/results.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        # Parse and sanitize query
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
            return context

        # Basic icontains search using existing queryset helpers
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
            .only("name", "slug", "country__name")
        )

        # Prepare combined results (will be paginated in brief-02)
        context["airport_results"] = airports
        context["city_results"] = cities
        context["results"] = list(airports) + list(cities)
        context["results_count"] = len(context["results"])

        return context
```

**Key Points:**

- **Safety:** `.strip()` removes leading/trailing whitespace; empty queries short-circuit to avoid unnecessary DB queries
- **Performance:** `select_related()` prevents N+1 queries; `.only()` limits fields fetched
- **Separation of Concerns:** Uses `.search(q)` methods defined on Airport and City QuerySets for DRY filtering logic

**3. Wire Up URLs with Namespacing**

File: `apps/search/urls.py`:

```python
from django.urls import path

from .views import SearchView

app_name = "search"
urlpatterns = [
    path("", SearchView.as_view(), name="index"),
]
```

File: `travelmathlite/core/urls.py` (add to urlpatterns):

```python
from django.urls import include, path

urlpatterns = [
    # ... existing patterns ...
    path("search/", include("apps.search.urls", namespace="search")),
]
```

**From Django Documentation on URL Namespacing:**

> URL namespaces allow you to uniquely identify URL patterns across multiple apps. Use `namespace` parameter in `include()` and reference in templates with `{% url 'namespace:name' %}`.

**4. Create Minimal Results Template**

File: `apps/search/templates/search/results.html`:

```django-html
{% extends "base.html" %}

{% block title %}Search{% if query %} — {{ query }}{% endif %}{% endblock %}

{% block content %}
  <h1>Search</h1>

  <form method="get" action="{% url 'search:index' %}" style="margin-bottom: 1rem;">
    <label for="q">Query</label>
    <input type="text" id="q" name="q" value="{{ query }}" />
    <button type="submit">Search</button>
  </form>

  {% if had_query %}
    <p><strong>{{ results_count }}</strong> result{{ results_count|pluralize }} for "{{ query }}"</p>

    {% if results %}
      <ul>
        {% for obj in results %}
          {% if obj.iata_code %}
            {# Airport #}
            <li>
              [Airport] {{ obj.name }} ({{ obj.iata_code }})
              {% if obj.municipality %} — {{ obj.municipality }}{% endif %}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% else %}
            {# City #}
            <li>
              [City] {{ obj.name }}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% endif %}
        {% endfor %}
      </ul>
    {% else %}
      <p>No results found.</p>
    {% endif %}
  {% else %}
    <p>Enter a query above to search for airports or cities.</p>
  {% endif %}
{% endblock %}
```

**Template Best Practices:**

- Always use `{% url %}` tag instead of hardcoded paths
- Include `value="{{ query }}"` to preserve user input on submission
- Use `pluralize` filter for proper grammar
- Type-check objects with conditional logic (airport vs city)

### Verification

```bash
# Run Django checks
uv run python travelmathlite/manage.py check

# Start development server
uv run python travelmathlite/manage.py runserver

# Test in browser:
# - http://127.0.0.1:8000/search/ (empty query)
# - http://127.0.0.1:8000/search/?q=Dallas (with results)
# - http://127.0.0.1:8000/search/?q=xyz (no results)

# Verify no DB queries on empty:
# Check Django Debug Toolbar or use --debug-sql
```

---

## Section 2: Pagination and Query String Preservation (Brief 02)

### Brief Context

Add Django's `Paginator` to handle large result sets. Ensure pagination controls preserve the `q` parameter so users can navigate pages without losing their search query.

### Django Concepts: Pagination

**From Matt Layman's "Understand Django" (Chapter: Views):**

> Django's Paginator class divides a list of items into pages. Combine with QuerySets to efficiently paginate database results without loading all rows into memory.

**From Django Documentation:**

> **Paginator and Page Objects:**
>
> ```python
> from django.core.paginator import Paginator
> 
> objects = ['john', 'paul', 'george', 'ringo']
> paginator = Paginator(objects, 2)  # 2 items per page
> 
> page = paginator.get_page(1)  # Returns Page object
> print(page.object_list)  # ['john', 'paul']
> print(page.has_next())  # True
> print(page.next_page_number())  # 2
> ```
>
> The `get_page()` method is safer than `page()` because it handles invalid page numbers gracefully (returns first or last page instead of raising PageNotAnInteger or EmptyPage).

### Implementation Steps

**1. Update SearchView to Use Paginator**

File: `apps/search/views.py` (update `get_context_data`):

```python
from django.core.paginator import Paginator, Page

class SearchView(TemplateView):
    template_name: str = "search/results.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        raw_q = self.request.GET.get("q", "")
        q = (raw_q or "").strip()

        context["query"] = q
        context["had_query"] = bool(q)

        if not q:
            context["results"] = []
            context["results_count"] = 0
            context["page_obj"] = None
            return context

        # Fetch airports and cities
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
            .only("name", "slug", "country__name")
        )

        # Combine as tuples for type differentiation in template
        results: list[tuple[str, Airport | City]] = [
            ("airport", a) for a in airports
        ] + [("city", c) for c in cities]

        # Pagination
        page_number = self.request.GET.get("page", 1)
        paginator = Paginator(results, 20)  # 20 items per page
        page_obj: Page = paginator.get_page(page_number)

        context["results"] = results
        context["results_count"] = len(results)
        context["page_obj"] = page_obj

        return context
```

**Key Changes:**

- Results are now tuples `(type_str, obj)` to distinguish airports from cities
- `Paginator` initialized with 20 items per page
- `page_obj` added to context for template use

**2. Update Template with Pagination Controls**

File: `apps/search/templates/search/results.html`:

```django-html
{% extends "base.html" %}

{% block title %}Search{% if query %} — {{ query }}{% endif %}{% endblock %}

{% block content %}
  <h1>Search</h1>

  <form method="get" action="{% url 'search:index' %}" style="margin-bottom: 1rem;">
    <label for="q">Query</label>
    <input type="text" id="q" name="q" value="{{ query }}" />
    <button type="submit">Search</button>
  </form>

  {% if had_query %}
    <p><strong>{{ results_count }}</strong> result{{ results_count|pluralize }} for "{{ query }}"</p>

    {% if page_obj %}
      <ul>
        {% for type_str, obj in page_obj %}
          {% if type_str == "airport" %}
            <li>
              [Airport] {{ obj.name }} ({{ obj.iata_code }})
              {% if obj.municipality %} — {{ obj.municipality }}{% endif %}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% else %}
            <li>
              [City] {{ obj.name }}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% endif %}
        {% endfor %}
      </ul>

      {# Pagination controls #}
      {% if page_obj.has_other_pages %}
        <nav aria-label="Search pagination">
          <ul>
            {% if page_obj.has_previous %}
              <li><a href="?q={{ query|urlencode }}&page=1">First</a></li>
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.previous_page_number }}">Previous</a></li>
            {% endif %}
            <li>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</li>
            {% if page_obj.has_next %}
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.next_page_number }}">Next</a></li>
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.paginator.num_pages }}">Last</a></li>
            {% endif %}
          </ul>
        </nav>
      {% endif %}
    {% endif %}
  {% else %}
    <p>Enter a query above to search for airports or cities.</p>
  {% endif %}
{% endblock %}
```

**Critical Detail: `urlencode` Filter**

**From Django Documentation:**

> The `urlencode` filter escapes strings for use in URL query parameters, converting spaces to `%20` and other special characters to percent-encoded equivalents.

**Why This Matters:**

- Without `urlencode`, a query like `"New York"` would create malformed URLs: `?q=New York&page=2`
- With `urlencode`, it becomes: `?q=New%20York&page=2`
- This preserves the query correctly across pagination

### Verification

```bash
# Create test data with enough results to paginate
uv run python travelmathlite/manage.py shell
>>> from apps.airports.models import Airport
>>> Airport.objects.filter(name__icontains="airport").count()
# Should be > 20 for pagination

# Test in browser:
# - http://127.0.0.1:8000/search/?q=airport
# - Click "Next" and verify URL includes ?q=airport&page=2
# - Verify query input remains filled
```

---

## Section 3: Highlight Helper and Safety (Brief 03)

### Brief Context

Create a custom template filter to highlight search query matches in results using `<mark>` tags. Ensure the filter properly escapes HTML to prevent XSS attacks while allowing the `<mark>` tag through.

### Django Concepts: Custom Template Filters and Auto-Escaping

**From Matt Layman's "Understand Django" (Chapter: Templates):**

> Django's template system auto-escapes variables to prevent XSS attacks. When you need to inject safe HTML, use Django's `mark_safe()` utility—but only after you've manually escaped user input.

**From Django Documentation:**

> **Creating Custom Template Filters:**
>
> ```python
> from django import template
> 
> register = template.Library()
> 
> @register.filter(needs_autoescape=True)
> def my_filter(value, arg, autoescape=True):
>     if autoescape:
>         from django.utils.html import conditional_escape
>         value = conditional_escape(value)
>     # ... process value ...
>     from django.utils.safestring import mark_safe
>     return mark_safe(result)
> ```
>
> The `needs_autoescape=True` parameter tells Django to pass the current autoescape context to your filter.

**Security Warning:**

> Never use `mark_safe()` on unescaped user input. Always escape first with `conditional_escape()`, then apply your safe HTML markup, then wrap with `mark_safe()`.

### Implementation Steps

**1. Create Template Tag Module**

File: `apps/search/templatetags/__init__.py`:

```python
# Empty file to make this a Python package
```

File: `apps/search/templatetags/search_extras.py`:

```python
from django import template

register = template.Library()

# Import filters from other modules
from .highlight import *  # noqa: F401, F403
```

**2. Implement Safe Highlight Filter**

File: `apps/search/templatetags/highlight.py`:

```python
from __future__ import annotations

import re

from django import template
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def highlight(text: str, query: str, autoescape: bool = True) -> SafeString:
    """Highlight query matches in text with <mark> tags.
    
    Safely escapes HTML in both text and query, then wraps matches with <mark>.
    
    Args:
        text: The text to search within
        query: The search query to highlight
        autoescape: Django's autoescape context (handled automatically)
        
    Returns:
        SafeString with matches wrapped in <mark> tags
        
    Example:
        {{ airport.name|highlight:query }}
        "Dallas Love Field" with query "Love" → "Dallas <mark>Love</mark> Field"
    """
    if not query:
        return conditional_escape(text) if autoescape else text

    # Escape both text and query to prevent XSS
    if autoescape:
        text = str(conditional_escape(text))
        query = str(conditional_escape(query))

    # Escape regex special characters in query
    escaped_query = re.escape(query)
    
    # Case-insensitive replacement
    pattern = re.compile(f"({escaped_query})", re.IGNORECASE)
    
    def replace_match(match):
        return format_html("<mark>{}</mark>", match.group(0))
    
    highlighted = pattern.sub(lambda m: replace_match(m), text)
    
    return mark_safe(highlighted)
```

**Security Analysis:**

1. **Escape First:** `conditional_escape(text)` converts `<script>` to `&lt;script&gt;`
2. **Escape Query:** `conditional_escape(query)` prevents regex injection
3. **Escape Regex Meta-chars:** `re.escape()` prevents `$`, `*`, etc. from being interpreted as regex
4. **Safe HTML Injection:** `format_html()` safely constructs `<mark>` tags
5. **Mark Safe:** Only after all escaping is done, we `mark_safe()` the result

**Why Not Just `mark_safe(text.replace(query, f"<mark>{query}</mark>"))`?**

- ❌ User input `<script>alert('xss')</script>` would execute
- ❌ Query `.*` would match entire string (regex injection)
- ✅ Our implementation escapes first, then injects only `<mark>` tags

**3. Load Filter in Template**

File: `apps/search/templates/search/results.html` (update):

```django-html
{% extends "base.html" %}
{% load search_extras %}

{% block title %}Search{% if query %} — {{ query }}{% endif %}{% endblock %}

{% block content %}
  <h1>Search</h1>

  <form method="get" action="{% url 'search:index' %}" style="margin-bottom: 1rem;">
    <label for="q">Query</label>
    <input type="text" id="q" name="q" value="{{ query }}" />
    <button type="submit">Search</button>
  </form>

  {% if had_query %}
    <p><strong>{{ results_count }}</strong> result{{ results_count|pluralize }} for "{{ query }}"</p>

    {% if page_obj %}
      <ul>
        {% for type_str, obj in page_obj %}
          {% if type_str == "airport" %}
            <li>
              [Airport] {{ obj.name|highlight:query }} ({{ obj.iata_code }})
              {% if obj.municipality %} — {{ obj.municipality|highlight:query }}{% endif %}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% else %}
            <li>
              [City] {{ obj.name|highlight:query }}
              {% if obj.country %}, {{ obj.country.name }}{% endif %}
            </li>
          {% endif %}
        {% endfor %}
      </ul>

      {# Pagination controls (unchanged) #}
      {% if page_obj.has_other_pages %}
        <nav aria-label="Search pagination">
          <ul>
            {% if page_obj.has_previous %}
              <li><a href="?q={{ query|urlencode }}&page=1">First</a></li>
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.previous_page_number }}">Previous</a></li>
            {% endif %}
            <li>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</li>
            {% if page_obj.has_next %}
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.next_page_number }}">Next</a></li>
              <li><a href="?q={{ query|urlencode }}&page={{ page_obj.paginator.num_pages }}">Last</a></li>
            {% endif %}
          </ul>
        </nav>
      {% endif %}
    {% endif %}
  {% else %}
    <p>Enter a query above to search for airports or cities.</p>
  {% endif %}
{% endblock %}
```

**Key Changes:**

- `{% load search_extras %}` at top
- `{{ obj.name|highlight:query }}` wraps matches in `<mark>`
- `<mark>` element is styled by browser (yellow background by default)

### Verification

```bash
# Test in browser:
# - http://127.0.0.1:8000/search/?q=Dallas
# - Verify "Dallas" is wrapped in <mark> tags
# - Inspect HTML to confirm proper escaping

# Security test - try XSS:
# - http://127.0.0.1:8000/search/?q=<script>alert('xss')</script>
# - Verify script tag is escaped and displayed as text, not executed
```

---

## Section 4: URL Design, Canonical Links, and Sitemap (Brief 04)

### Brief Context

Establish friendly URL patterns using Django's `reverse()` everywhere. Add canonical link tags to result pages for SEO. Configure sitemap and robots.txt to help search engines discover key pages.

### Django Concepts: URL Reversing and SEO

**From Matt Layman's "Understand Django" (Chapter: URLs):**

> Never hardcode URLs in your templates or views. Use the `reverse()` function and `{% url %}` template tag to generate URLs dynamically from your URL configuration. This makes your app portable and easier to refactor.

**From Django Documentation on Sitemaps:**

> **Django Sitemap Framework:**
>
> Sitemaps are XML files that tell search engines about pages on your site. Django provides `django.contrib.sitemaps` to generate sitemaps automatically.
>
> ```python
> from django.contrib.sitemaps import Sitemap
> from django.urls import reverse
> 
> class StaticViewSitemap(Sitemap):
>     priority = 0.5
>     changefreq = 'daily'
>     
>     def items(self):
>         return ['main:index', 'blog:posts']
>     
>     def location(self, item):
>         return reverse(item)
> ```

**SEO Best Practices:**

- **Canonical URLs:** Tell search engines which URL is the "official" version when multiple URLs show the same content
- **Sitemap:** Helps search engines discover all pages on your site
- **Robots.txt:** Instructs search engine crawlers which paths to crawl or avoid

### Implementation Steps

**1. Add Canonical Block to Base Template**

File: `travelmathlite/templates/base.html` (add to `<head>`):

```django-html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}travelmathlite{% endblock %}</title>
    {% block canonical %}{% endblock %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
  </head>
  <body>
    <!-- ... rest of template ... -->
  </body>
</html>
```

**2. Add Canonical Link to Search Results**

File: `apps/search/templates/search/results.html` (add after `{% extends %}`):

```django-html
{% extends "base.html" %}
{% load search_extras %}

{% block title %}Search{% if query %} — {{ query }}{% endif %}{% endblock %}

{% block canonical %}
  {% if had_query %}
    <link rel="canonical" href="{{ request.scheme }}://{{ request.get_host }}{% url 'search:index' %}?q={{ query|urlencode }}{% if page_obj.number > 1 %}&page={{ page_obj.number }}{% endif %}" />
  {% endif %}
{% endblock %}

{% block content %}
  <!-- ... existing content ... -->
{% endblock %}
```

**Why This Canonical URL?**

- Includes query parameter: `?q={{ query|urlencode }}`
- Includes page number if not page 1: `&page={{ page_obj.number }}`
- Prevents duplicate content issues when same search appears at different URLs
- Search engines treat `?q=Dallas` and `?q=Dallas&page=1` as same page

**3. Create Sitemap Configuration**

File: `travelmathlite/core/sitemaps.py`:

```python
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static/core views."""
    
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return [
            "base:index",
            "search:index",
            "airports:index",
            "airports:nearest",
            "calculators:index",
        ]

    def location(self, item):
        return reverse(item)
```

**4. Wire Sitemap to URLs**

File: `travelmathlite/core/urls.py`:

```python
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
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
```

**5. Create robots.txt Template**

File: `travelmathlite/templates/robots.txt`:

```
User-agent: *
Disallow: /admin/

Sitemap: {{ request.scheme }}://{{ request.get_host }}/sitemap.xml
```

**Note:** This is a Django template, not static text, so it dynamically generates the sitemap URL.

### Verification

```bash
# Verify sitemap
curl http://127.0.0.1:8000/sitemap.xml
# Should see XML with URLs for base:index, search:index, etc.

# Verify robots.txt
curl http://127.0.0.1:8000/robots.txt
# Should see User-agent, Disallow, and Sitemap directives

# Verify canonical in search results
curl http://127.0.0.1:8000/search/?q=Dallas
# Inspect <head> for <link rel="canonical" ...>

# Run Django checks
uv run python travelmathlite/manage.py check
```

---

## Section 5: Templates and Navbar Search (Brief 05)

### Brief Context

Integrate a Bootstrap 5 navbar with an embedded search form. Update base template to use `{% url %}` template tags everywhere instead of hardcoded paths. Ensure the search form preserves the query value after submission.

### Bootstrap Concepts: Navbar Component

**From Bootstrap 5 Documentation:**

> **Navbar:** A responsive navigation header with support for branding, navigation, forms, and more. Use `.navbar-expand-{breakpoint}` to control when the navbar collapses.
>
> ```html
> <nav class="navbar navbar-expand-lg bg-body-tertiary">
>   <div class="container-fluid">
>     <a class="navbar-brand" href="#">Brand</a>
>     <button class="navbar-toggler" ...>
>       <span class="navbar-toggler-icon"></span>
>     </button>
>     <div class="collapse navbar-collapse">
>       <ul class="navbar-nav me-auto">
>         <li class="nav-item"><a class="nav-link" href="#">Link</a></li>
>       </ul>
>       <form class="d-flex">
>         <input class="form-control me-2" type="search">
>         <button class="btn btn-outline-success" type="submit">Search</button>
>       </form>
>     </div>
>   </div>
> </nav>
> ```

**Key Bootstrap Classes:**

- `.navbar-expand-lg`: Collapse navbar on screens smaller than "large"
- `.navbar-toggler`: Hamburger button for collapsed state
- `.d-flex`: Flexbox layout for search form
- `.me-2`: Margin-end (right) spacing

### Implementation Steps

#### 1. Update Base Template with Bootstrap Navbar

File: `travelmathlite/templates/base.html`:

```django-html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}travelmathlite{% endblock %}</title>
    {% block canonical %}{% endblock %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <script src="https://unpkg.com/htmx.org@1.9.12" integrity="sha384-NSnJQ8c8uMaVn+qjJ1JQkZkQwH6R1a2KqUmiB9rVx3z0wqG9pWZ1lCw1Jf3YB5V" crossorigin="anonymous"></script>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="{% url 'base:index' %}">TravelMathLite</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="{% url 'base:index' %}">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'calculators:index' %}">Calculators</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'airports:index' %}">Airports</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'airports:nearest' %}">Nearest</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'accounts:index' %}">Accounts</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'trips:index' %}">Trips</a>
            </li>
          </ul>
          <form class="d-flex" role="search" method="get" action="{% url 'search:index' %}">
            <input class="form-control me-2" type="search" name="q" placeholder="Search airports or cities" aria-label="Search" value="{{ request.GET.q }}">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav>
    <main class="container my-4">
      {% block content %}{% endblock %}
    </main>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
  </body>
</html>
```

**Key Improvements:**

- **All links use `{% url %}`:** Portable across URL changes
- **Search form in navbar:** Always accessible from any page
- **`value="{{ request.GET.q }}"`:** Preserves query after search (works on all pages)
- **Bootstrap JS:** Required for navbar collapse toggle
- **`.container` main:** Consistent content width with responsive padding

**Why `request.GET.q` Instead of `query`?**

- `request.GET.q` is available globally in all templates via request context processor
- `query` is only available in SearchView's context
- Using `request.GET.q` means the navbar search form shows the query on all pages

### Verification

```bash
# Start server
uv run python travelmathlite/manage.py runserver

# Test navbar search:
# 1. Go to http://127.0.0.1:8000/ (home page)
# 2. Type "Dallas" in navbar search and submit
# 3. Should redirect to /search/?q=Dallas
# 4. Verify navbar search input still shows "Dallas"
# 5. Navigate to any other page - navbar search should still show "Dallas"

# Test responsive collapse:
# - Resize browser window to mobile width
# - Click hamburger button
# - Verify menu expands/collapses
```

---

## Section 6: Tests and Visual Checks (Brief 06)

### Brief Context

Write comprehensive tests for search functionality covering query parsing, pagination, highlighting safety, and canonical links. Create a Playwright visual check script for automated screenshot capture.

### Django Concepts: Testing with TestCase

**From Matt Layman's "Understand Django" (Chapter: Testing):**

> Django's `TestCase` class provides a test database that's created before each test and destroyed after. Use `self.client.get()` to simulate HTTP requests and `assertContains()` to verify response content.

**From Django Documentation:**

> **Writing Tests:**
>
> ```python
> from django.test import TestCase
> from django.urls import reverse
> 
> class MyViewTests(TestCase):
>     def test_view_url_accessible_by_name(self):
>         response = self.client.get(reverse('myapp:myview'))
>         self.assertEqual(response.status_code, 200)
>         
>     def test_view_uses_correct_template(self):
>         response = self.client.get(reverse('myapp:myview'))
>         self.assertTemplateUsed(response, 'myapp/myview.html')
> ```

### Implementation Steps

**1. Create Comprehensive Test Suite**

File: `apps/search/tests.py`:

```python
from django.test import TestCase
from django.urls import reverse

from ..airports.models import Airport
from ..base.models import City, Country
from .templatetags.highlight import highlight


class SearchViewTests(TestCase):
    def setUp(self) -> None:
        """Create test data: country, city, and airport."""
        self.country = Country.objects.create(
            iso_code="US",
            name="United States",
            search_name="united states",
            slug="united-states",
        )
        self.city = City.objects.create(
            country=self.country,
            name="Dallas",
            slug="dallas",
        )
        self.airport = Airport.objects.create(
            ident="KDAL",
            iata_code="DAL",
            name="Dallas Love Field",
            municipality="Dallas",
            iso_country="US",
            country=self.country,
            city=self.city,
            latitude_deg=32.8470,
            longitude_deg=-96.8517,
        )

    def test_search_no_query_returns_empty(self) -> None:
        """Empty query should return no results."""
        url = reverse("search:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "search/results.html")
        self.assertEqual(resp.context["results_count"], 0)
        self.assertFalse(resp.context["had_query"])

    def test_search_with_query_returns_results(self) -> None:
        """Valid query should return matching airport."""
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["had_query"])
        self.assertEqual(resp.context["query"], "Dallas")
        self.assertGreater(resp.context["results_count"], 0)

    def test_pagination_preserves_query_string(self) -> None:
        """Pagination links should preserve the query parameter."""
        # Create enough airports to trigger pagination (20 items per page)
        for i in range(25):
            Airport.objects.create(
                ident=f"TEST{i:02d}",
                iata_code=f"T{i:02d}",
                name=f"Test Airport {i}",
                municipality="TestCity",
                iso_country="US",
                country=self.country,
                city=self.city,
                latitude_deg=32.0 + (i * 0.1),
                longitude_deg=-96.0 + (i * 0.1),
            )

        url = reverse("search:index") + "?q=Test"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["page_obj"].has_next())

        # Check that pagination links include the query
        self.assertContains(resp, "?q=Test&page=2")

    def test_canonical_link_in_results(self) -> None:
        """Results page should include canonical link with query."""
        url = reverse("search:index") + "?q=Dallas"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<link rel="canonical"')
        self.assertContains(resp, "?q=Dallas")


class HighlightFilterTests(TestCase):
    def test_highlight_wraps_match_in_mark_tags(self) -> None:
        """Highlight filter should wrap matches in <mark> tags."""
        result = highlight("Dallas Love Field", "Love")
        self.assertIn("<mark>Love</mark>", result)

    def test_highlight_escapes_html_in_text(self) -> None:
        """Highlight filter should escape HTML entities in text."""
        result = highlight("<script>alert('xss')</script>", "script")
        self.assertIn("&lt;", result)
        self.assertIn("&gt;", result)
        self.assertNotIn("<script>", result)

    def test_highlight_escapes_regex_special_chars_in_query(self) -> None:
        """Highlight filter should escape regex special characters in query."""
        result = highlight("Cost is $100", "$100")
        self.assertIn("<mark>$100</mark>", result)

    def test_highlight_case_insensitive(self) -> None:
        """Highlight filter should be case-insensitive."""
        result = highlight("Dallas Love Field", "love")
        self.assertIn("<mark>Love</mark>", result)

    def test_highlight_empty_query_returns_original(self) -> None:
        """Empty query should return original text escaped."""
        result = highlight("Dallas Love Field", "")
        self.assertEqual(result, "Dallas Love Field")

    def test_highlight_no_match_returns_escaped_text(self) -> None:
        """No match should return escaped text without marks."""
        result = highlight("Dallas Love Field", "Houston")
        self.assertEqual(result, "Dallas Love Field")
        self.assertNotIn("<mark>", result)
```

**Test Coverage Analysis:**

- **SearchView:** Empty query handling, query parsing, pagination, canonical links
- **Highlight Filter:** XSS prevention, regex escaping, case-insensitivity, edge cases

**2. Run Tests**

```bash
# Run all search tests
uv run python travelmathlite/manage.py test apps.search

# Run with verbose output
uv run python travelmathlite/manage.py test apps.search --verbosity=2

# Expected output: All tests pass
```

**3. Create Visual Check Script**

File: `travelmathlite/scripts/visual_check_search.py`:

```python
"""Visual regression check for search feature.

Captures screenshots of search flows for manual/automated visual inspection.
Run with: python scripts/visual_check_search.py (after: playwright install chromium)
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright


def wait_for_port(host: str, port: int, timeout: float = 25.0) -> bool:
    """Poll until the given port is listening or timeout expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.5)
            try:
                if sock.connect_ex((host, port)) == 0:
                    return True
            except OSError:
                pass
        time.sleep(0.25)
    return False


def main() -> int:
    # Project root is the travelmathlite folder containing manage.py
    project_root = Path(__file__).resolve().parents[1]
    manage_py = project_root / "manage.py"
    screenshots_dir = project_root / "screenshots" / "search"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    host = os.environ.get("VISUAL_CHECK_HOST", "127.0.0.1")
    port = int(os.environ.get("VISUAL_CHECK_PORT", "8010"))
    base_url = f"http://{host}:{port}"

    # Start Django dev server
    server = subprocess.Popen(
        [sys.executable, str(manage_py), "runserver", f"{host}:{port}"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        if not wait_for_port(host, port, timeout=30):
            print("ERROR: Django dev server did not start in time.")
            try:
                outs, _ = server.communicate(timeout=1)
                if outs:
                    print(outs)
            except subprocess.TimeoutExpired:
                pass
            return 1

        print(f"✓ Django server ready at {base_url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            # Test 1: Empty search page
            print("Capturing: empty search page...")
            page.goto(f"{base_url}/search/")
            page.screenshot(path=str(screenshots_dir / "01-empty-search.png"))

            # Test 2: Search from navbar on home page
            print("Capturing: navbar search from home...")
            page.goto(f"{base_url}/")
            page.fill('input[name="q"]', "Dallas")
            page.screenshot(path=str(screenshots_dir / "02-navbar-search-filled.png"))
            page.click('button[type="submit"]')
            page.wait_for_url(f"{base_url}/search/?q=Dallas")
            page.screenshot(path=str(screenshots_dir / "03-search-results-dallas.png"))

            # Test 3: Pagination (if enough results)
            print("Capturing: search with pagination...")
            page.goto(f"{base_url}/search/?q=Airport")
            page.screenshot(path=str(screenshots_dir / "04-search-results-airport.png"))

            # Check if pagination exists and navigate to page 2
            if page.locator('a:has-text("2")').count() > 0:
                page.click('a:has-text("2")')
                page.wait_for_load_state("networkidle")
                page.screenshot(path=str(screenshots_dir / "05-search-results-page2.png"))

            browser.close()

        print(f"✓ Screenshots saved to {screenshots_dir}")
        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


if __name__ == "__main__":
    sys.exit(main())
```

**4. Install Playwright and Run Visual Check**

```bash
# Install Playwright browsers
uv run playwright install chromium

# Run visual check
uv run python travelmathlite/scripts/visual_check_search.py

# Check screenshots
ls travelmathlite/screenshots/search/
# Should see:
# - 01-empty-search.png
# - 02-navbar-search-filled.png
# - 03-search-results-dallas.png
# - 04-search-results-airport.png
# - 05-search-results-page2.png (if pagination exists)
```

### Verification

```bash
# Run all tests
uv run python travelmathlite/manage.py test apps.search

# Expected output:
# Ran 10 tests in X.XXs
# OK

# Run visual check
uv run python travelmathlite/scripts/visual_check_search.py

# Verify screenshots visually
# - Check for Bootstrap navbar rendering
# - Verify search highlights (yellow <mark> background)
# - Confirm pagination controls display correctly
```

---

## Summary and Key Takeaways

### What We Built

1. **Search View:** Case-insensitive `icontains` filtering across airports and cities
2. **Pagination:** 20 results per page with query string preservation
3. **Highlighting:** Safe HTML injection with XSS protection
4. **SEO:** Canonical links, sitemap.xml, robots.txt
5. **UI:** Bootstrap 5 navbar with integrated search form
6. **Testing:** 10 tests covering functionality and security

### Django Patterns Applied

- **Custom QuerySets:** Encapsulated search logic in `Airport.objects.search()` and `City.objects.search()`
- **TemplateView:** Clean separation of concerns with `get_context_data()`
- **Custom Template Filters:** Safe HTML rendering with `needs_autoescape=True`
- **URL Namespacing:** All links use `{% url 'namespace:name' %}` for portability
- **Django Pagination:** Efficient large result handling with `Paginator`

### Security Considerations

- **XSS Prevention:** All user input escaped before rendering
- **Regex Injection:** Query strings escaped with `re.escape()`
- **SQL Injection:** Protected by Django ORM's parameterized queries
- **HTML Injection:** `conditional_escape()` → safe HTML → `mark_safe()` pattern

### Performance Optimizations

- **Select Related:** Avoid N+1 queries with `select_related("country", "city")`
- **Only:** Fetch only needed fields with `.only()`
- **Early Return:** Empty queries skip database hits
- **Bounding Box:** (In nearest lookup) Pre-filter before expensive haversine calculations

### Next Steps

- **Enhanced Search:** Add fuzzy matching with trigram similarity (Postgres)
- **Autocomplete:** HTMX-powered typeahead suggestions
- **Faceted Search:** Filter by country, type, or distance
- **Search Analytics:** Track popular queries for optimization
- **Full-Text Search:** Upgrade to Postgres FTS or Elasticsearch for larger datasets

---

## Full References

### Django Documentation

- [QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Pagination](https://docs.djangoproject.com/en/stable/topics/pagination/)
- [Custom Template Tags and Filters](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/)
- [URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Sitemap Framework](https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/)
- [Testing Tools](https://docs.djangoproject.com/en/stable/topics/testing/tools/)

### Matt Layman's "Understand Django"

- [Models and Databases](https://www.mattlayman.com/understand-django/models-and-databases/)
- [Views, Templates, and Forms](https://www.mattlayman.com/understand-django/)
- [URL Routing](https://www.mattlayman.com/understand-django/urls-lead-way/)
- [Testing](https://www.mattlayman.com/understand-django/test-your-apps/)

### Bootstrap 5 Documentation

- [Navbar Component](https://getbootstrap.com/docs/5.3/components/navbar/)
- [Pagination Component](https://getbootstrap.com/docs/5.3/components/pagination/)
- [Forms](https://getbootstrap.com/docs/5.3/forms/overview/)

### Additional Resources

- [HTMX Documentation](https://htmx.org/docs/)
- [Playwright Python](https://playwright.dev/python/docs/intro)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [uv Package Manager](https://github.com/astral-sh/uv)

---

**Tutorial Version:** 1.0  
**Last Updated:** 2025-11-16  
**Tested Against:** Django 5.2.7, Python 3.13, Bootstrap 5.3.3
