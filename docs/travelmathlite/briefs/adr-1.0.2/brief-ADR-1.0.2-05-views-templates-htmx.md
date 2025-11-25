# BRIEF: Build views, templates, and HTMX partials slice

Goal

- Implement calculator views and templates with HTMX partials for interactive results addressing PRD §4 F-001, F-003.

Scope (single PR)

- Files to touch: `apps/calculators/views.py`, `apps/calculators/templates/`, `apps/calculators/urls.py`, base template updates.
- Non-goals: Backend calculation logic (already implemented), form definitions (already implemented).

Standards

- Commits: conventional style (feat/fix/docs/refactor/test/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).
- Prefer CBVs for form handling; FBVs ok for HTMX partials.

Acceptance

- User flow: User fills form, submits, sees results rendered via HTMX without full page reload.
- Results show distance (flight and driving), driving time, and cost (if cost calculator).
- Unit display matches user selection (km/miles).
- Include migration? no
- Update docs & PR checklist.

Deliverables

- [ ] `calculators/views.py`:
  - `DistanceCalculatorView` (CBV, FormView or TemplateView with form handling)
  - `CostCalculatorView` (CBV)
  - `distance_result_partial` (FBV for HTMX response)
  - `cost_result_partial` (FBV for HTMX response)
- [ ] Templates:
  - `calculators/distance_calculator.html`: form layout, HTMX target div
  - `calculators/cost_calculator.html`: form layout, HTMX target div
  - `calculators/partials/distance_result.html`: result display (flight distance, driving distance, driving time)
  - `calculators/partials/cost_result.html`: result display (distance, time, fuel cost)
- [ ] URL routing in `calculators/urls.py`
- [ ] Link calculators in base template navigation or home page
- [ ] Tests:
  - GET requests render forms
  - POST with valid data returns results (test both full page and HTMX partial)
  - POST with invalid data re-renders form with errors

Prompts for Copilot

- "Generate Django CBV for distance calculator in `calculators/views.py`. Use FormView pattern: on GET render form, on POST validate and render results via HTMX partial. Import DistanceCalculatorForm and geo module."
- "Generate Django template `calculators/distance_calculator.html` with form, HTMX attributes (hx-post, hx-target), and result div."
- "Generate HTMX partial template `calculators/partials/distance_result.html` that displays flight distance, driving distance estimate, and driving time with proper units."
- "Generate similar CBV and templates for cost calculator."
- "Add URL patterns to `calculators/urls.py` with namespace 'calculators'."
- "Create Django TestCase for views: test GET renders form, test POST with valid data, test POST with invalid data, test HTMX partial responses."
- "Propose commit messages for views, templates, and HTMX integration."

---
ADR: adr-1.0.2-geo-calculation-methods.md
PRD: §4 F-001, F-003, §7 NF-001 (performance)
Issue: #TODO
