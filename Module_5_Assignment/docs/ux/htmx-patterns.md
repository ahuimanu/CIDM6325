# HTMX Patterns and Progressive Enhancement

**Last updated:** 2025-11-16  
**ADR:** adr-1.0.5-forms-and-htmx-progressive-enhancement.md  
**Status:** Active

---

## Overview

TravelMathLite uses HTMX to enhance forms with partial updates while maintaining full progressive enhancement. All features work without JavaScript, with HTMX providing a better user experience when available.

## HTMX Configuration

### Base Template Integration

HTMX is loaded globally via CDN in `templates/base.html`:

```html
<script src="https://unpkg.com/htmx.org@2.0.3" 
        integrity="sha384-0895/pl2MU10Hqc6jd4RvrthNlDiE9U1tWmX7WRESftEDRosgxNsQG/Ze9YMRzHq" 
        crossorigin="anonymous"></script>
```

**Version:** 2.0.3 (latest stable as of implementation)  
**CDN:** unpkg.com  
**Fallback:** All forms work with standard POST/GET when HTMX is unavailable

### Content Security Policy (CSP)

If CSP headers are configured, ensure the following directives are present:

```
script-src 'self' https://unpkg.com https://cdn.jsdelivr.net;
```

Currently, no CSP headers are configured in the application.

---

## Progressive Enhancement Strategy

### Core Principle

Every HTMX-enhanced feature must work without JavaScript. HTMX is an **enhancement**, not a requirement.

### Implementation Pattern

1. **Build the standard flow first** - Full POST/GET with page reloads
2. **Add HTMX attributes** - `hx-post`, `hx-target`, `hx-swap`
3. **Create partial templates** - For HTMX responses only
4. **Update views** - Detect HTMX and conditionally return partials
5. **Test both flows** - With and without JavaScript

---

## HTMX Attribute Patterns

### Form Submission with Partial Update

```html
<form method="post" action="{% url 'calculators:distance' %}"
      hx-post="{% url 'calculators:distance' %}"
      hx-target="#result-container"
      hx-swap="outerHTML">
  {% csrf_token %}
  <!-- form fields -->
  <button type="submit">Calculate</button>
</form>

<div id="result-container">
  <!-- Results appear here -->
</div>
```

**Key points:**

- `method="post"` and `action` provide fallback behavior
- `hx-post` enables HTMX submission
- `hx-target` specifies where to insert response
- `hx-swap="outerHTML"` replaces the target element entirely

### CSRF Token Handling

Django CSRF tokens work automatically with HTMX when:

1. `{% csrf_token %}` is present in the form
2. HTMX is loaded after Django's CSRF setup (already satisfied)

HTMX automatically includes the CSRF token in AJAX requests.

---

## View Pattern: Dual-Mode Rendering

### Single View for Both Flows

**Invariant (INV-1):** Same view handles both HTMX and full-page requests.

```python
def calculator_view(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            result = perform_calculation(form.cleaned_data)
            context = {'form': form, 'result': result}
            
            # Detect HTMX request
            if request.headers.get('HX-Request'):
                # Return partial template for HTMX
                return render(request, 'calculators/partials/result.html', context)
            
            # Return full page for standard POST
            return render(request, 'calculators/calculator.html', context)
    else:
        form = CalculatorForm()
    
    return render(request, 'calculators/calculator.html', {'form': form})
```

**Detection:** `request.headers.get('HX-Request')` returns `'true'` for HTMX requests.

---

## Template Organization

### Directory Structure

```
apps/calculators/templates/calculators/
├── distance_calculator.html       # Full page template
├── cost_calculator.html           # Full page template
└── partials/
    ├── distance_result.html       # HTMX partial
    └── cost_result.html            # HTMX partial
```

### Shared Blocks and Includes

To avoid duplication between full and partial templates, use Django template inheritance:

```django
{# calculators/partials/distance_result.html #}
<div id="result-container" class="card mt-3">
  {% include 'calculators/_result_content.html' %}
</div>

{# calculators/distance_calculator.html #}
<div id="result-container">
  {% if result %}
    {% include 'calculators/_result_content.html' %}
  {% endif %}
</div>
```

---

## Accessibility Considerations

### Focus Management

After HTMX swaps content, focus should move to the updated region:

```html
<div id="result-container" 
     tabindex="-1"
     hx-swap="outerHTML focus-scroll:true">
  <!-- Results -->
</div>
```

Alternative using HTMX events:

```html
<script>
document.body.addEventListener('htmx:afterSwap', function(evt) {
  if (evt.detail.target.id === 'result-container') {
    evt.detail.target.focus();
  }
});
</script>
```

### ARIA Live Regions

For screen reader announcements:

```html
<div id="result-container" 
     aria-live="polite" 
     aria-atomic="true">
  <!-- Results announced to screen readers when updated -->
</div>
```

**Note:** `aria-live="polite"` waits for screen reader to finish current announcement before interrupting.

### Keyboard Navigation

Ensure all interactive elements remain keyboard-accessible after HTMX swaps:

- Buttons should remain focusable
- Form fields should maintain tab order
- Links should be reachable via keyboard

---

## Testing HTMX Flows

### Unit Tests (Django TestCase)

```python
from django.test import TestCase, RequestFactory

class CalculatorViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_htmx_request_returns_partial(self):
        """HTMX requests should return partial template"""
        request = self.factory.post('/calculator/', data={...})
        request.headers = {'HX-Request': 'true'}
        response = calculator_view(request)
        self.assertTemplateUsed(response, 'calculators/partials/result.html')
    
    def test_standard_request_returns_full_page(self):
        """Standard POST should return full page"""
        request = self.factory.post('/calculator/', data={...})
        response = calculator_view(request)
        self.assertTemplateUsed(response, 'calculators/calculator.html')
```

### Manual Testing

1. **With JavaScript enabled:** Verify HTMX partial updates work
2. **With JavaScript disabled:** Verify full page reloads work
3. **With keyboard only:** Verify focus management and navigation
4. **With screen reader:** Verify announcements for dynamic updates

### Visual Checks (Playwright)

Automated visual regression tests are available in `travelmathlite/scripts/`:

**Run HTMX calculator visual checks:**

```bash
# Install Playwright browser (one-time setup)
uvx playwright install chromium

# Run the visual check script
cd travelmathlite
python scripts/visual_check_htmx_calculators.py
```

**What it tests:**

- Distance calculator with HTMX (empty, filled, result, validation errors)
- Cost calculator with HTMX (empty, filled, result)
- No-JS fallback behavior (full page reloads)
- Screenshots saved to `travelmathlite/screenshots/calculators/`

**Scripts available:**

- `visual_check_htmx_calculators.py` - HTMX calculator flows (ADR-1.0.5)
- `visual_check_search.py` - Search feature flows (ADR-1.0.4)

---

## Troubleshooting

### HTMX Not Loading

Check browser console for:

- Network errors loading script from CDN
- CSP violations blocking script execution
- `typeof htmx !== 'undefined'` should return `true` in console

### CSRF Token Errors

Ensure:

- `{% csrf_token %}` is present in all forms
- Django middleware includes `CsrfViewMiddleware`
- HTMX script loads after page load (already satisfied in base template)

### Partial Template Not Rendering

Check:

- View correctly detects `HX-Request` header
- Partial template path is correct
- Template includes necessary context variables

---

## References

- **HTMX Documentation:** <https://htmx.org/docs/>
- **Django CSRF:** <https://docs.djangoproject.com/en/stable/ref/csrf/>
- **WCAG 2.1 AA:** <https://www.w3.org/WAI/WCAG21/quickref/>
- **ADR-1.0.5:** docs/travelmathlite/adr/adr-1.0.5-forms-and-htmx-progressive-enhancement.md
- **PRD:** docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-16 | 1.0 | Initial documentation for ADR-1.0.5-01 |
| 2025-11-16 | 1.1 | Added focus management, visual check script documentation (ADR-1.0.5-05, ADR-1.0.5-06) |
