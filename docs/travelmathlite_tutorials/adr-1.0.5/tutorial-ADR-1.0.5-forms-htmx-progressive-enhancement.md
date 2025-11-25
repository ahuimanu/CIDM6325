# Tutorial: ADR-1.0.5 Forms and HTMX Progressive Enhancement Implementation

## Goal

Learn how TravelMathLite implements progressive enhancement with HTMX for calculator forms, providing a snappy user experience while maintaining full no-JS fallback. This tutorial walks through adding HTMX attributes to existing Django forms, implementing partial templates, detecting HTMX requests in views, and ensuring accessibility—all while preserving the simplicity of Django's form processing and CSRF protection.

## Context and Traceability

- **ADR:** `docs/travelmathlite/adr/adr-1.0.5-forms-and-htmx-progressive-enhancement.md`
- **Briefs:** `docs/travelmathlite/briefs/adr-1.0.5/` (six briefs covering base setup → forms → partials → views → accessibility → tests)
- **Apps:** `travelmathlite/apps/calculators/`
- **PRD Requirements:** §4 F-001 (distance calculator), §4 F-003 (cost calculator), §4 F-007 (templates), §7 NF-002 (accessibility)
- **Functional Requirements:** FR-F-001-2 (form validation), FR-F-003-1 (defaults and errors), FR-F-007-1 (templates)
- **Non-Functional Requirements:** NF-002 (accessibility with focus management and ARIA)

## Prerequisites

Before starting this tutorial, ensure you have:

- TravelMathLite project initialized with `uv` (see ADR-1.0.0 tutorial)
- Python 3.13+ environment activated
- Database migrated with airport models
- Airport data loaded via `import_airports` management command (see ADR-1.0.1 tutorial)
- Bootstrap 5.3.3 included in base template
- Working calculator forms for distance and cost (from earlier ADRs)
- Basic familiarity with:
  - Django forms and form validation
  - Django template rendering and `{% include %}`
  - Django view patterns for detecting request headers
  - Bootstrap 5 components (cards, forms, buttons)
  - HTMX basics (attributes like `hx-post`, `hx-target`, `hx-swap`)
  - Web accessibility (ARIA live regions, focus management)

## Section 1: HTMX Base Template Integration (Brief 01)

### Brief Context

Add HTMX script to the base template and configure global focus management. This provides the foundation for all HTMX interactions across the application while ensuring accessibility features work correctly after partial page updates.

### HTMX Concepts: Progressive Enhancement and Events

**From HTMX Documentation:**

> HTMX allows you to access modern browser features directly from HTML, rather than using JavaScript. It extends HTML with attributes like `hx-post`, `hx-get`, `hx-target`, and `hx-swap` to enable AJAX, CSS Transitions, WebSockets, and Server Sent Events without writing custom JavaScript.
>
> **Progressive Enhancement:** HTMX works by intercepting form submissions and link clicks, making AJAX requests, and swapping the response into the DOM. If JavaScript is disabled, forms fall back to standard HTTP POST/GET flows.

**From HTMX Documentation on Events:**

> HTMX emits events during its request/response lifecycle:
>
> - `htmx:beforeRequest` — Before an AJAX request is made
> - `htmx:afterSwap` — After new content has been swapped into the DOM
> - `htmx:afterSettle` — After all settle tasks have completed
>
> You can listen for these events to add custom behavior like focus management or analytics.

**From Web Content Accessibility Guidelines (WCAG) 2.1:**

> **Focus Management:** When content is added or updated dynamically, keyboard users must be able to navigate to the new content. Use `tabindex="-1"` to make non-interactive elements focusable programmatically, then call `.focus()` to direct keyboard focus.

### Implementation Steps

**1. Add HTMX Script with Integrity Hash**

File: `travelmathlite/templates/base.html` (add before closing `</body>`):

```django-html
    <!-- HTMX for progressive enhancement -->
    <script 
      src="https://unpkg.com/htmx.org@2.0.3" 
      integrity="sha384-0895/pl2MU10Hqc6jd4RvrthNlDiE9U1tWmX7WRESftEDRosgxNsQG/Ze9YMRzHq" 
      crossorigin="anonymous">
    </script>

    <!-- Focus management: after HTMX swaps, move focus to result if present -->
    <script>
      document.body.addEventListener('htmx:afterSwap', function(event) {
        // Look for an element with data-focus="true" in the swapped content
        const focusTarget = event.detail.target.querySelector('[data-focus="true"]');
        if (focusTarget) {
          focusTarget.focus();
        }
      });
    </script>
  </body>
</html>
```

**Key Points:**

- **Integrity Hash:** Ensures the HTMX library hasn't been tampered with (Subresource Integrity)
- **Version 2.0.3:** Latest stable release as of implementation
- **Focus Management:** `htmx:afterSwap` event listener moves keyboard focus to results after partial updates
- **Progressive Enhancement:** If JavaScript is disabled, HTMX never loads and forms work normally

**2. Verify HTMX Loads Correctly**

Start the development server:

```bash
cd travelmathlite
uv run python manage.py runserver
```

Open your browser's developer console and check for:

```
HTMX version 2.0.3 loaded successfully
```

**From Django Documentation on Static Files:**

> Django templates can reference external CDN resources directly in HTML. For production, consider downloading HTMX and serving it as a static file to avoid external dependencies.

### Verification Steps

- [ ] HTMX script loads without console errors
- [ ] `htmx:afterSwap` event listener registered
- [ ] Base template renders correctly for existing pages

---

## Section 2: HTMX-Enhanced Calculator Forms (Brief 02)

### Brief Context

Add HTMX attributes to distance and cost calculator forms. Forms will submit via AJAX when JavaScript is enabled, but fall back to standard POST when disabled. This implements the core progressive enhancement pattern.

### Django and HTMX Integration

**From Matt Layman's "Understand Django" (Chapter: Forms):**

> Django forms handle both GET (initial display) and POST (submission). The same view can render an empty form, process submissions, and display validation errors. HTMX extends this pattern by allowing partial template responses without changing the view logic.

**From HTMX Documentation on Form Submission:**

> **hx-post:** Issues a POST request to the specified URL when triggered (typically by form submission)
>
> **hx-target:** Specifies the element to swap content into (CSS selector)
>
> **hx-swap:** Defines how to swap the response (`innerHTML`, `outerHTML`, `beforeend`, etc.)
>
> ```html
> <form hx-post="/submit" hx-target="#results" hx-swap="innerHTML">
>   <!-- form fields -->
> </form>
> ```

**Django CSRF with HTMX:**

> Django's `{% csrf_token %}` template tag works automatically with HTMX. HTMX includes the CSRF token in POST requests, so no additional configuration is needed.

### Implementation Steps

**1. Enhance Distance Calculator Form**

File: `travelmathlite/apps/calculators/templates/calculators/distance_calculator.html`:

```django-html
{% extends "base.html" %}

{% block title %}Distance Calculator{% endblock %}

{% block content %}
  <div class="row">
    <div class="col-md-6">
      <h1>Distance Calculator</h1>
      <p class="text-muted">Calculate distance between two airports.</p>

      <form 
        method="post" 
        action="{% url 'calculators:distance' %}"
        hx-post="{% url 'calculators:distance' %}"
        hx-target="#distance-result"
        hx-swap="innerHTML">
        
        {% csrf_token %}
        
        <div class="mb-3">
          {{ form.from_lat.label_tag }}
          {{ form.from_lat }}
          {% if form.from_lat.errors %}
            <div class="text-danger">{{ form.from_lat.errors }}</div>
          {% endif %}
        </div>

        <div class="mb-3">
          {{ form.from_lon.label_tag }}
          {{ form.from_lon }}
          {% if form.from_lon.errors %}
            <div class="text-danger">{{ form.from_lon.errors }}</div>
          {% endif %}
        </div>

        <div class="mb-3">
          {{ form.to_lat.label_tag }}
          {{ form.to_lat }}
          {% if form.to_lat.errors %}
            <div class="text-danger">{{ form.to_lat.errors }}</div>
          {% endif %}
        </div>

        <div class="mb-3">
          {{ form.to_lon.label_tag }}
          {{ form.to_lon }}
          {% if form.to_lon.errors %}
            <div class="text-danger">{{ form.to_lon.errors }}</div>
          {% endif %}
        </div>

        <button type="submit" class="btn btn-primary">Calculate Distance</button>
      </form>
    </div>

    <div class="col-md-6">
      <div id="distance-result">
        <!-- HTMX will swap results here; initial content on full page load -->
        {% if distance %}
          {% include "calculators/partials/distance_result.html" %}
        {% endif %}
      </div>
    </div>
  </div>
{% endblock %}
```

**Key Points:**

- **Dual Submission:** `action` attribute handles no-JS fallback; `hx-post` handles HTMX flow
- **Same URL:** Both `action` and `hx-post` point to the same view (INV-1: same view for both flows)
- **Target Region:** `#distance-result` div receives partial responses
- **CSRF Protection:** `{% csrf_token %}` works for both HTMX and standard POST
- **Bootstrap Classes:** `mb-3` for spacing, `text-danger` for errors, `btn btn-primary` for submit button

**2. Enhance Cost Calculator Form**

File: `travelmathlite/apps/calculators/templates/calculators/cost_calculator.html`:

```django-html
{% extends "base.html" %}

{% block title %}Cost Calculator{% endblock %}

{% block content %}
  <div class="row">
    <div class="col-md-6">
      <h1>Trip Cost Calculator</h1>
      <p class="text-muted">Estimate trip cost based on distance and price per mile.</p>

      <form 
        method="post" 
        action="{% url 'calculators:cost' %}"
        hx-post="{% url 'calculators:cost' %}"
        hx-target="#cost-result"
        hx-swap="innerHTML">
        
        {% csrf_token %}
        
        <div class="mb-3">
          {{ form.distance_miles.label_tag }}
          {{ form.distance_miles }}
          {% if form.distance_miles.errors %}
            <div class="text-danger">{{ form.distance_miles.errors }}</div>
          {% endif %}
        </div>

        <div class="mb-3">
          {{ form.price_per_mile.label_tag }}
          {{ form.price_per_mile }}
          {% if form.price_per_mile.errors %}
            <div class="text-danger">{{ form.price_per_mile.errors }}</div>
          {% endif %}
        </div>

        <button type="submit" class="btn btn-primary">Calculate Cost</button>
      </form>
    </div>

    <div class="col-md-6">
      <div id="cost-result">
        <!-- HTMX will swap results here; initial content on full page load -->
        {% if total_cost %}
          {% include "calculators/partials/cost_result.html" %}
        {% endif %}
      </div>
    </div>
  </div>
{% endblock %}
```

**Key Points:**

- **Consistent Pattern:** Same structure as distance calculator for maintainability
- **Semantic HTML:** Proper `<label>` tags for accessibility
- **Bootstrap Grid:** `row` and `col-md-6` for responsive two-column layout

### Verification Steps

- [ ] Forms submit with full page reload when JavaScript is disabled
- [ ] Forms submit via AJAX when JavaScript is enabled (check Network tab)
- [ ] CSRF token present in both flows
- [ ] Bootstrap styling applied correctly

---

## Section 3: Partial Templates for HTMX Responses (Brief 03)

### Brief Context

Create partial templates for distance and cost results. These templates are used both for HTMX partial responses and for initial full-page renders via `{% include %}`. They must be self-contained, accessible, and visually consistent with Bootstrap cards.

### Django Template Includes

**From Django Documentation on Template Inheritance:**

> The `{% include %}` tag loads a template and renders it with the current context. This is useful for reusing template fragments across different pages.
>
> ```django-html
> {% include "partials/result.html" %}
> ```

**From Bootstrap 5 Documentation on Cards:**

> Cards are flexible content containers with multiple variants and options. Use `.card`, `.card-body`, `.card-title`, and `.card-text` for basic structure.
>
> ```html
> <div class="card">
>   <div class="card-body">
>     <h5 class="card-title">Title</h5>
>     <p class="card-text">Content here.</p>
>   </div>
> </div>
> ```

**From WAI-ARIA Best Practices:**

> **Live Regions:** Use `aria-live="polite"` for dynamic content updates that don't require immediate user attention. Screen readers will announce the change after completing the current task.
>
> **Focus Management:** Use `tabindex="-1"` on headings or containers that should receive programmatic focus but aren't normally interactive.

### Implementation Steps

**1. Create Partials Directory**

```bash
cd travelmathlite/apps/calculators/templates/calculators
mkdir -p partials
```

**2. Distance Result Partial**

File: `travelmathlite/apps/calculators/templates/calculators/partials/distance_result.html`:

```django-html
<div class="card" aria-live="polite" data-focus="true" tabindex="-1">
  <div class="card-body">
    {% if distance %}
      <h2 class="card-title h4">Distance Result</h2>
      <p class="card-text">
        <strong>{{ distance|floatformat:2 }} miles</strong>
      </p>
      <p class="card-text text-muted">
        From ({{ from_lat }}, {{ from_lon }}) to ({{ to_lat }}, {{ to_lon }})
      </p>
    {% else %}
      <h2 class="card-title h4 text-danger">Error</h2>
      <p class="card-text">
        Unable to calculate distance. Please check your coordinates and try again.
      </p>
    {% endif %}
  </div>
</div>
```

**Key Points:**

- **ARIA Live Region:** `aria-live="polite"` announces updates to screen readers
- **Focus Target:** `data-focus="true"` marks this element for programmatic focus (connected to base template's `htmx:afterSwap` listener)
- **Focusable Non-Interactive:** `tabindex="-1"` allows `.focus()` call without adding to tab order
- **Bootstrap Card:** Semantic card structure with title and text
- **Error Handling:** Shows error message when `distance` is `None`
- **Float Formatting:** `|floatformat:2` rounds to 2 decimal places

**3. Cost Result Partial**

File: `travelmathlite/apps/calculators/templates/calculators/partials/cost_result.html`:

```django-html
<div class="card" aria-live="polite" data-focus="true" tabindex="-1">
  <div class="card-body">
    {% if total_cost %}
      <h2 class="card-title h4">Cost Estimate</h2>
      <p class="card-text">
        <strong>${{ total_cost|floatformat:2 }}</strong>
      </p>
      <p class="card-text text-muted">
        Based on {{ distance_miles }} miles at ${{ price_per_mile|floatformat:2 }}/mile
      </p>
    {% else %}
      <h2 class="card-title h4 text-danger">Error</h2>
      <p class="card-text">
        Unable to calculate cost. Please check your inputs and try again.
      </p>
    {% endif %}
  </div>
</div>
```

**Key Points:**

- **Consistent Structure:** Matches distance partial for visual consistency
- **Currency Formatting:** `${{ total_cost|floatformat:2 }}` displays as currency
- **Context Display:** Shows input values for transparency
- **Accessibility:** Same ARIA and focus management patterns

### Verification Steps

- [ ] Partial templates render correctly when included in full templates
- [ ] ARIA attributes present (`aria-live="polite"`)
- [ ] Focus management attributes present (`data-focus="true"`, `tabindex="-1"`)
- [ ] Bootstrap card styling applied
- [ ] Error states display appropriately

---

## Section 4: View HTMX Detection and Partial Rendering (Brief 04)

### Brief Context

Update calculator views to detect HTMX requests via the `HX-Request` header and render partial templates accordingly. This allows the same view to handle both full-page and AJAX requests without duplication (INV-1).

### Django Request Headers

**From Django Documentation on HttpRequest:**

> The `request.headers` attribute is a case-insensitive dictionary-like object that provides access to all HTTP headers.
>
> ```python
> # Check for custom header
> if request.headers.get('X-Custom-Header'):
>     # Handle custom header
> ```

**From HTMX Documentation on Request Headers:**

> HTMX includes several headers in its AJAX requests:
>
> - `HX-Request`: Always `true` for HTMX requests
> - `HX-Target`: The `id` of the target element
> - `HX-Trigger`: The `id` of the element that triggered the request
>
> Use these headers to conditionally return partial HTML instead of full pages.

**From Matt Layman's "Understand Django" (Chapter: Views):**

> Views should return `HttpResponse` objects. Use `render()` as a shortcut to render a template with context. The same view can return different templates based on request properties.

### Implementation Steps

**1. Update Distance Calculator View**

File: `travelmathlite/apps/calculators/views.py`:

```python
from __future__ import annotations

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from .forms import CostCalculatorForm, DistanceCalculatorForm
from .utils import calculate_distance, calculate_trip_cost


class DistanceCalculatorView(FormView):
    """Calculate distance between two geographic coordinates.
    
    Supports both full-page and HTMX partial rendering based on HX-Request header.
    """
    
    template_name = "calculators/distance_calculator.html"
    form_class = DistanceCalculatorForm
    
    def form_valid(self, form: DistanceCalculatorForm) -> HttpResponse:
        """Process valid form and return appropriate response."""
        # Extract and calculate
        from_lat = form.cleaned_data["from_lat"]
        from_lon = form.cleaned_data["from_lon"]
        to_lat = form.cleaned_data["to_lat"]
        to_lon = form.cleaned_data["to_lon"]
        
        distance = calculate_distance(from_lat, from_lon, to_lat, to_lon)
        
        context = {
            "form": form,
            "distance": distance,
            "from_lat": from_lat,
            "from_lon": from_lon,
            "to_lat": to_lat,
            "to_lon": to_lon,
        }
        
        # Detect HTMX and return partial if present
        if self.request.headers.get("HX-Request"):
            return render(
                self.request, 
                "calculators/partials/distance_result.html", 
                context
            )
        
        # Full page reload for non-HTMX requests
        return render(self.request, self.template_name, context)
    
    def form_invalid(self, form: DistanceCalculatorForm) -> HttpResponse:
        """Handle invalid form submission."""
        context = {"form": form, "distance": None}
        
        # HTMX: return partial with error state
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "calculators/partials/distance_result.html",
                context
            )
        
        # Full page with form errors
        return render(self.request, self.template_name, context)


class CostCalculatorView(FormView):
    """Calculate trip cost based on distance and price per mile.
    
    Supports both full-page and HTMX partial rendering based on HX-Request header.
    """
    
    template_name = "calculators/cost_calculator.html"
    form_class = CostCalculatorForm
    
    def form_valid(self, form: CostCalculatorForm) -> HttpResponse:
        """Process valid form and return appropriate response."""
        distance_miles = form.cleaned_data["distance_miles"]
        price_per_mile = form.cleaned_data["price_per_mile"]
        
        total_cost = calculate_trip_cost(distance_miles, price_per_mile)
        
        context = {
            "form": form,
            "total_cost": total_cost,
            "distance_miles": distance_miles,
            "price_per_mile": price_per_mile,
        }
        
        # Detect HTMX and return partial if present
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "calculators/partials/cost_result.html",
                context
            )
        
        # Full page reload for non-HTMX requests
        return render(self.request, self.template_name, context)
    
    def form_invalid(self, form: CostCalculatorForm) -> HttpResponse:
        """Handle invalid form submission."""
        context = {"form": form, "total_cost": None}
        
        # HTMX: return partial with error state
        if self.request.headers.get("HX-Request"):
            return render(
                self.request,
                "calculators/partials/cost_result.html",
                context
            )
        
        # Full page with form errors
        return render(self.request, self.template_name, context)
```

**Key Points:**

- **Single View Pattern:** One view handles both HTMX and full-page requests (INV-1)
- **Header Detection:** `request.headers.get("HX-Request")` checks for HTMX
- **Conditional Templates:** Returns partial or full template based on request type
- **Error Handling:** `form_invalid()` also supports both flows
- **Type Hints:** Added for clarity and IDE support
- **Context Reuse:** Same context variables work for both templates

**From Django CBV Documentation:**

> `FormView` provides a convenient pattern for processing forms. Override `form_valid()` for successful submissions and `form_invalid()` for validation errors.

### Verification Steps

- [ ] HTMX requests return partial templates (check Network tab → Response)
- [ ] Non-HTMX requests return full templates
- [ ] Form validation works in both modes
- [ ] Error states render correctly in partial responses
- [ ] No CSRF errors in either flow

---

## Section 5: Focus Management and Accessibility (Brief 05)

### Brief Context

Verify that focus management works correctly after HTMX swaps, ensuring keyboard and screen reader users can navigate to updated content. This brief validates the integration between the base template's `htmx:afterSwap` listener and the partial templates' `data-focus="true"` attributes.

### Accessibility Fundamentals

**From WCAG 2.1 Success Criterion 2.4.3 (Focus Order):**

> If a Web page can be navigated sequentially and the navigation sequences affect meaning or operation, focusable components receive focus in an order that preserves meaning and operability.

**From WCAG 2.1 Success Criterion 4.1.3 (Status Messages):**

> Status messages can be programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus.

**From MDN Web Docs on ARIA Live Regions:**

> `aria-live="polite"` indicates that updates to the region should be presented at the next graceful opportunity, such as at the end of speaking the current sentence or when the user pauses typing.

### Implementation Steps

**1. Manual Keyboard Testing**

Open the distance calculator and test keyboard navigation:

1. Tab to the first input field
2. Fill out all fields using only keyboard
3. Press Enter to submit
4. **Expected:** Focus moves to the result card automatically
5. Press Tab → **Expected:** Focus moves to next interactive element

**2. Screen Reader Testing (Optional)**

Using NVDA (Windows) or VoiceOver (Mac):

1. Navigate to distance calculator
2. Fill form and submit
3. **Expected:** Screen reader announces "Distance Result" heading
4. **Expected:** Screen reader reads result content

**3. No-JS Fallback Testing**

Disable JavaScript in browser DevTools:

1. Open DevTools → Settings → Disable JavaScript
2. Reload calculator page
3. Submit form
4. **Expected:** Full page reload with results visible
5. **Expected:** Focus returns to top of page (standard browser behavior)

### Verification Code

The following elements work together for accessibility:

**Base Template Event Listener** (`templates/base.html`):

```javascript
document.body.addEventListener('htmx:afterSwap', function(event) {
  const focusTarget = event.detail.target.querySelector('[data-focus="true"]');
  if (focusTarget) {
    focusTarget.focus();
  }
});
```

**Partial Template Focus Target** (`partials/distance_result.html`):

```django-html
<div class="card" aria-live="polite" data-focus="true" tabindex="-1">
  <!-- result content -->
</div>
```

**How It Works:**

1. User submits form via HTMX
2. Server returns partial HTML
3. HTMX swaps content into `#distance-result` div
4. HTMX fires `htmx:afterSwap` event
5. Event listener finds `[data-focus="true"]` element
6. `.focus()` moves keyboard focus to result card
7. Screen reader announces content via `aria-live="polite"`

### Verification Steps

- [ ] Focus moves to result card after HTMX swap (keyboard test)
- [ ] Screen reader announces result (optional, if available)
- [ ] Tab order remains logical after focus move
- [ ] No-JS fallback works without focus management
- [ ] No console errors related to focus

---

## Section 6: Tests and Visual Checks (Brief 06)

### Brief Context

Write comprehensive unit tests for both HTMX and non-HTMX flows, plus a Playwright visual check script to capture screenshots. This ensures the progressive enhancement pattern works correctly and provides regression testing artifacts.

### Django Testing with RequestFactory

**From Django Documentation on Testing:**

> Django's `RequestFactory` provides a way to generate request instances that can be used directly in view testing. It's lighter than the test client because it doesn't execute middleware or URL routing.
>
> ```python
> from django.test import RequestFactory, TestCase
>
> class ViewTests(TestCase):
>     def setUp(self):
>         self.factory = RequestFactory()
>     
>     def test_view(self):
>         request = self.factory.post('/path/', data={'key': 'value'})
>         response = my_view(request)
>         self.assertEqual(response.status_code, 200)
> ```

**From Django Documentation on assertContains:**

> `assertContains()` asserts that a response contains a given value in its content. It also checks that the response status code is 200.
>
> ```python
> self.assertContains(response, 'Expected text')
> ```

### Implementation Steps

**1. Unit Tests for Calculator Views**

File: `travelmathlite/apps/calculators/tests.py` (add to existing tests):

```python
from django.test import RequestFactory, TestCase

from .views import CostCalculatorView, DistanceCalculatorView


class DistanceCalculatorHTMXTests(TestCase):
    """Test HTMX-specific behavior for distance calculator."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_htmx_request_returns_partial(self):
        """HTMX requests should return partial template."""
        request = self.factory.post(
            "/calculators/distance/",
            data={
                "from_lat": "33.4484",
                "from_lon": "-112.0740",
                "to_lat": "40.7128",
                "to_lon": "-74.0060",
            },
            HTTP_HX_REQUEST="true",
        )
        view = DistanceCalculatorView.as_view()
        response = view(request)

        # Should return partial, not full template
        self.assertContains(response, "Distance Result")
        self.assertContains(response, "aria-live")
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_non_htmx_request_returns_full_page(self):
        """Standard POST should return full template."""
        request = self.factory.post(
            "/calculators/distance/",
            data={
                "from_lat": "33.4484",
                "from_lon": "-112.0740",
                "to_lat": "40.7128",
                "to_lon": "-74.0060",
            },
        )
        view = DistanceCalculatorView.as_view()
        response = view(request)

        # Should include full page structure
        self.assertContains(response, "Distance Calculator")
        self.assertContains(response, "Distance Result")

    def test_htmx_invalid_form_returns_error_partial(self):
        """HTMX request with invalid data returns error partial."""
        request = self.factory.post(
            "/calculators/distance/",
            data={"from_lat": "invalid"},  # Invalid latitude
            HTTP_HX_REQUEST="true",
        )
        view = DistanceCalculatorView.as_view()
        response = view(request)

        self.assertContains(response, "Error")
        self.assertContains(response, "aria-live")


class CostCalculatorHTMXTests(TestCase):
    """Test HTMX-specific behavior for cost calculator."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_htmx_request_returns_partial(self):
        """HTMX requests should return partial template."""
        request = self.factory.post(
            "/calculators/cost/",
            data={"distance_miles": "100", "price_per_mile": "0.50"},
            HTTP_HX_REQUEST="true",
        )
        view = CostCalculatorView.as_view()
        response = view(request)

        self.assertContains(response, "Cost Estimate")
        self.assertContains(response, "$50.00")
        self.assertContains(response, "aria-live")
        self.assertNotContains(response, "<!DOCTYPE html>")

    def test_non_htmx_request_returns_full_page(self):
        """Standard POST should return full template."""
        request = self.factory.post(
            "/calculators/cost/",
            data={"distance_miles": "100", "price_per_mile": "0.50"},
        )
        view = CostCalculatorView.as_view()
        response = view(request)

        self.assertContains(response, "Trip Cost Calculator")
        self.assertContains(response, "Cost Estimate")

    def test_htmx_invalid_form_returns_error_partial(self):
        """HTMX request with invalid data returns error partial."""
        request = self.factory.post(
            "/calculators/cost/",
            data={"distance_miles": "-50"},  # Negative distance invalid
            HTTP_HX_REQUEST="true",
        )
        view = CostCalculatorView.as_view()
        response = view(request)

        self.assertContains(response, "Error")
        self.assertContains(response, "aria-live")


class CalculatorCSRFTests(TestCase):
    """Ensure CSRF tokens present in forms (INV-2)."""

    def test_distance_form_has_csrf(self):
        """Distance calculator form includes CSRF token."""
        response = self.client.get("/calculators/distance/")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_cost_form_has_csrf(self):
        """Cost calculator form includes CSRF token."""
        response = self.client.get("/calculators/cost/")
        self.assertContains(response, "csrfmiddlewaretoken")
```

**Key Points:**

- **HTTP_HX_REQUEST:** Simulates HTMX header in test requests
- **assertContains:** Checks response content and status code
- **assertNotContains:** Verifies partial doesn't include full HTML structure
- **CSRF Validation:** Ensures security tokens present (INV-2)
- **Error Cases:** Tests invalid form data in both flows

**2. Run Tests**

```bash
cd travelmathlite
uv run python manage.py test apps.calculators.tests
```

**Expected Output:**

```
.......
----------------------------------------------------------------------
Ran 7 tests in 0.123s

OK
```

**3. Playwright Visual Check Script**

File: `travelmathlite/scripts/visual_check_htmx_calculators.py`:

```python
#!/usr/bin/env python
"""Visual check for HTMX calculator interactions.

Captures screenshots of:
1. Distance calculator: empty, filled, result, error
2. Cost calculator: empty, filled, result, error
3. No-JS fallback: distance calculator full page reload
4. No-JS fallback: cost calculator full page reload

Screenshots saved to: travelmathlite/screenshots/calculators/
"""

from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    """Run visual checks and capture screenshots."""
    base_url = "http://127.0.0.1:8000"
    screenshot_dir = Path(__file__).parent.parent / "screenshots" / "calculators"
    screenshot_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Distance Calculator: Empty state
        page.goto(f"{base_url}/calculators/distance/")
        page.wait_for_load_state("networkidle")
        page.screenshot(path=screenshot_dir / "01-distance-empty.png")

        # Distance Calculator: Filled form
        page.fill('input[name="from_lat"]', "33.4484")
        page.fill('input[name="from_lon"]', "-112.0740")
        page.fill('input[name="to_lat"]', "40.7128")
        page.fill('input[name="to_lon"]', "-74.0060")
        page.screenshot(path=screenshot_dir / "02-distance-filled.png")

        # Distance Calculator: HTMX result
        page.click('button[type="submit"]')
        page.wait_for_selector('[data-focus="true"]', timeout=5000)
        page.screenshot(path=screenshot_dir / "03-distance-result-htmx.png")

        # Distance Calculator: Error state (invalid input)
        page.fill('input[name="from_lat"]', "999")  # Invalid latitude
        page.click('button[type="submit"]')
        page.wait_for_timeout(1000)
        page.screenshot(path=screenshot_dir / "04-distance-error.png")

        # Cost Calculator: Empty state
        page.goto(f"{base_url}/calculators/cost/")
        page.wait_for_load_state("networkidle")
        page.screenshot(path=screenshot_dir / "05-cost-empty.png")

        # Cost Calculator: Filled form
        page.fill('input[name="distance_miles"]', "100")
        page.fill('input[name="price_per_mile"]', "0.50")
        page.screenshot(path=screenshot_dir / "06-cost-filled.png")

        # Cost Calculator: HTMX result
        page.click('button[type="submit"]')
        page.wait_for_selector('[data-focus="true"]', timeout=5000)
        page.screenshot(path=screenshot_dir / "07-cost-result-htmx.png")

        # Cost Calculator: Error state
        page.fill('input[name="distance_miles"]', "-50")  # Negative distance
        page.click('button[type="submit"]')
        page.wait_for_timeout(1000)
        page.screenshot(path=screenshot_dir / "08-cost-error.png")

        browser.close()

        # No-JS fallback testing (new context with JS disabled)
        browser_no_js = p.chromium.launch(headless=True)
        context_no_js = browser_no_js.new_context(java_script_enabled=False)
        page_no_js = context_no_js.new_page()

        # Distance Calculator: No-JS full page reload
        page_no_js.goto(f"{base_url}/calculators/distance/")
        page_no_js.wait_for_load_state("networkidle")
        page_no_js.fill('input[name="from_lat"]', "33.4484")
        page_no_js.fill('input[name="from_lon"]', "-112.0740")
        page_no_js.fill('input[name="to_lat"]', "40.7128")
        page_no_js.fill('input[name="to_lon"]', "-74.0060")
        page_no_js.click('button[type="submit"]')
        page_no_js.wait_for_load_state("networkidle")
        page_no_js.screenshot(path=screenshot_dir / "09-distance-no-js-result.png")

        # Cost Calculator: No-JS full page reload
        page_no_js.goto(f"{base_url}/calculators/cost/")
        page_no_js.wait_for_load_state("networkidle")
        page_no_js.fill('input[name="distance_miles"]', "100")
        page_no_js.fill('input[name="price_per_mile"]', "0.50")
        page_no_js.click('button[type="submit"]')
        page_no_js.wait_for_load_state("networkidle")
        page_no_js.screenshot(path=screenshot_dir / "10-cost-no-js-result.png")

        browser_no_js.close()

        print(f"✓ Visual checks complete. Screenshots saved to {screenshot_dir}")


if __name__ == "__main__":
    main()
```

**Key Points:**

- **Headless Mode:** Runs without opening browser window
- **Network Idle:** Waits for HTMX requests to complete
- **Selector Wait:** `wait_for_selector('[data-focus="true"]')` ensures HTMX swap finished
- **No-JS Context:** `java_script_enabled=False` tests fallback
- **10 Screenshots:** Comprehensive coverage of both calculators and both flows

**4. Run Visual Check Script**

First, start the development server in one terminal:

```bash
cd travelmathlite
uv run python manage.py runserver
```

Then run the visual check in another terminal:

```bash
cd travelmathlite
uv run python scripts/visual_check_htmx_calculators.py
```

**Expected Output:**

```
✓ Visual checks complete. Screenshots saved to /path/to/travelmathlite/screenshots/calculators
```

**5. Review Screenshots**

Navigate to `travelmathlite/screenshots/calculators/` and verify:

- **01-distance-empty.png:** Empty form with proper layout
- **02-distance-filled.png:** Form with coordinates entered
- **03-distance-result-htmx.png:** Result card visible on right side (no page reload)
- **04-distance-error.png:** Error state displayed
- **05-cost-empty.png:** Empty cost calculator
- **06-cost-filled.png:** Filled cost inputs
- **07-cost-result-htmx.png:** Cost result via HTMX
- **08-cost-error.png:** Cost validation error
- **09-distance-no-js-result.png:** Distance result after full page reload (no HTMX)
- **10-cost-no-js-result.png:** Cost result after full page reload (no HTMX)

### Verification Steps

- [ ] All 7 unit tests pass
- [ ] HTMX tests verify partial templates returned
- [ ] CSRF tests confirm tokens present
- [ ] Visual script runs without errors
- [ ] 10 screenshots captured successfully
- [ ] Screenshots show correct behavior for both JS and no-JS flows

---

## Summary and Key Takeaways

### What You Learned

1. **Progressive Enhancement Pattern:**
   - HTMX enhances forms with AJAX while preserving no-JS fallback
   - Same view handles both flows via header detection (INV-1)
   - `action` attribute provides fallback; `hx-post` enables enhancement

2. **HTMX Integration:**
   - Include HTMX script with integrity hash in base template
   - Use `hx-post`, `hx-target`, `hx-swap` attributes on forms
   - Detect HTMX requests via `HX-Request` header
   - Return partial templates for HTMX, full templates otherwise

3. **Accessibility:**
   - `aria-live="polite"` for screen reader announcements
   - `data-focus="true"` + `tabindex="-1"` for focus management
   - `htmx:afterSwap` event listener moves focus to results
   - Maintain logical tab order after partial updates

4. **Testing Strategy:**
   - Unit tests with `HTTP_HX_REQUEST` header simulate HTMX
   - `assertContains` validates partial vs full template responses
   - Playwright visual checks capture regression evidence
   - No-JS testing validates fallback behavior

### Invariants Enforced

- **INV-1:** Same view handles HTMX and non-HTMX requests (no duplicate endpoints)
- **INV-2:** CSRF tokens present in all forms (security)

### Files Modified

```
travelmathlite/
├── templates/
│   └── base.html                                          # HTMX script + focus listener
├── apps/calculators/
│   ├── templates/calculators/
│   │   ├── distance_calculator.html                       # HTMX attributes added
│   │   ├── cost_calculator.html                           # HTMX attributes added
│   │   └── partials/
│   │       ├── distance_result.html                       # New: partial with ARIA
│   │       └── cost_result.html                           # New: partial with ARIA
│   ├── views.py                                           # HTMX detection added
│   └── tests.py                                           # 7 new HTMX tests
├── scripts/
│   └── visual_check_htmx_calculators.py                   # New: Playwright script
└── screenshots/calculators/                               # 10 screenshots
```

### Documentation Created

- **docs/ux/htmx-patterns.md:** Comprehensive HTMX patterns and examples

### Next Steps

- **ADR-1.0.6 (hypothetical):** Extend HTMX to search results pagination
- **Optimization:** Add loading indicators with `hx-indicator`
- **Advanced HTMX:** Implement debouncing for search-as-you-type
- **Deployment:** Serve HTMX from static files instead of CDN

### Common Pitfalls to Avoid

1. **Separate endpoints for HTMX and full-page:** Violates INV-1, creates duplication
2. **Missing CSRF tokens:** Django will reject POST requests
3. **Forgetting `aria-live`:** Screen reader users won't know content updated
4. **Not testing no-JS fallback:** Progressive enhancement requires fallback validation
5. **Using `hx-get` for forms:** Forms should POST to maintain REST semantics

### Further Reading

- **HTMX Documentation:** <https://htmx.org/docs/>
- **HTMX Examples:** <https://htmx.org/examples/>
- **Django Class-Based Views:** <https://docs.djangoproject.com/en/stable/topics/class-based-views/>
- **WCAG 2.1 (Accessibility):** <https://www.w3.org/WAI/WCAG21/quickref/>
- **Matt Layman's Understand Django:** <https://www.mattlayman.com/understand-django/>

---

**Tutorial Complete!** You now have a production-ready progressive enhancement pattern using HTMX with Django forms, complete with accessibility features, comprehensive tests, and visual regression evidence.
