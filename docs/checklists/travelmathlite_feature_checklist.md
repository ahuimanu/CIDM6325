# travelmathlite Feature Checklist

> Generated from PRD Section 4: Scope items and checklist seeds
> File: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md

For each feature: check completion, validate acceptance notes, link artifacts, and record test status/date.

---

- [ ] F-001 Distance calculator (city/airport/coord)
  - User story: As a traveler I want to compute distance and driving time between two places so that I can plan a trip
  - Acceptance notes:
    - AC1 Support input by city name, airport code, or lat/long
    - AC2 Show driving distance/time and straight-line (flight) distance
    - AC3 HTMX submit updates results without full page reload; progressive enhancement preserves full form POST/GET
    - AC4 Persist last inputs in session for quick repeat
  - Artifacts: apps/calculators/, templates/calculators/, calculators/views.py, forms.py
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-002 Nearest airport lookup
  - User story: As a traveler I want the nearest airport to a city or coordinate so that I can choose flights
  - Acceptance notes:
    - AC1 Input city or coordinates return nearest airport with distance
    - AC2 Show a short list of top 3 airports sorted by distance
    - AC3 Link to airport detail page
  - Artifacts: apps/airports/, airports/views.py, templates/airports/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-003 Cost of driving estimator
  - User story: As a traveler I want an estimated fuel cost so that I can budget
  - Acceptance notes:
    - AC1 Inputs: distance (km/mi), fuel economy, fuel price
    - AC2 Defaults via settings; override per request via HTMX
    - AC3 Currency and units displayed consistently; form validation errors shown
  - Artifacts: calculators/costs.py, calculators/forms.py, templates/calculators/partials/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-004 Place and airport data models
  - User story: As a developer I want normalized models so that queries are fast and maintainable
  - Acceptance notes:
    - AC1 Models: City, Airport, Country with indexes on lookups
    - AC2 Custom manager for published/active records and case-insensitive search
    - AC3 Admin: list_display, search_fields, list_filter; CSV import action
  - Artifacts: apps/core/models.py, apps/airports/models.py, admin configs, migrations/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-005 Data import command
  - User story: As an operator I want a command to load seed datasets so that the app is usable
  - Acceptance notes:
    - AC1 Management command `import_airports` idempotent with --dry-run
    - AC2 Logs progress and handles retries; validates row counts
    - AC3 Supports file path argument and remote URL
  - Artifacts: apps/airports/management/commands/import_airports.py
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-006 Accounts and saved trips
  - User story: As a user I want to save recent calculations so that I can reuse them
  - Acceptance notes:
    - AC1 Auth: login/logout, registration; use Django auth views
    - AC2 Save last 10 calculations per user; list and delete
    - AC3 Session remembers last anonymous inputs; migrate on login
  - Artifacts: apps/accounts/, apps/trips/, templates/accounts/, templates/trips/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-007 Site navigation, layout, and branding
  - User story: As a user I want a clean responsive UI so that I can use the app on any device
  - Acceptance notes:
    - AC1 Base template with Bootstrap 5; navbar, footer; sticky footer
    - AC2 Static assets via collectstatic; favicon, CSS bundle
    - AC3 Accessibility: color contrast, focus states, ARIA on forms
  - Artifacts: templates/base.html, templates/includes/, static/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-008 Search and URL design
  - User story: As a user I want friendly URLs and search so that pages are shareable and discoverable
  - Acceptance notes:
    - AC1 Namespaced URLs with reversing everywhere
    - AC2 Search cities/airports by name/code with pagination; highlight results
    - AC3 Robots, sitemap, canonical links for key pages
  - Artifacts: urls.py, apps/search/views.py, templates/search/
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-009 Middleware and request tracing
  - User story: As an operator I want timing and correlation IDs so that I can debug issues
  - Acceptance notes:
    - AC1 Custom middleware adds X-Request-ID and logs duration
    - AC2 Security and common middleware configured; GZip or ConditionalGet
    - AC3 Health endpoint returns OK with commit SHA
  - Artifacts: core/middleware.py, settings, urls.py
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-010 Static and media management
  - User story: As an operator I want reliable static and media handling so that deploys are stable
  - Acceptance notes:
    - AC1 STATICFILES_DIRS and app static organized; collectstatic required
    - AC2 ManifestStaticFilesStorage enabled in prod
    - AC3 MEDIA configured; optional user avatar upload on profile
  - Artifacts: settings, static/, media/, accounts/forms.py
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-011 Testing and CI signals
  - User story: As a developer I want confidence in changes so that regressions are caught
  - Acceptance notes:
    - AC1 Django TestCase coverage for calculators, search, and auth flows
    - AC2 RequestFactory and assertTemplateUsed employed
    - AC3 Mock external calls; deterministically freeze time in tests
  - Artifacts: apps/*/tests.py, coverage report, CI config
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-012 Deployment-ready settings
  - User story: As an operator I want safe defaults so that production is secure
  - Acceptance notes:
    - AC1 Split settings: base/local/prod; DEBUG=False in prod; ALLOWED_HOSTS set
    - AC2 Env var parsing via django-environ and secrets sourced securely
    - AC3 Security headers configured; HTTPS ready
  - Artifacts: project/settings/{base,local,prod}.py
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-013 Performance and caching
  - User story: As a user I want fast responses so that the app feels snappy
  - Acceptance notes:
    - AC1 Use select_related/prefetch_related and indexes on hot paths
    - AC2 Enable per-view/low-level caching on search and airport endpoints
    - AC3 Cache headers for static/dynamic responses as appropriate
  - Artifacts: code annotations, settings caches, middleware
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-014 Security posture
  - User story: As an operator I want common risks mitigated so that user data is protected
  - Acceptance notes:
    - AC1 CSRF and input sanitization verified; templates autoescape; bleach where needed
    - AC2 Auth hardening with validators; admin access restricted; 2FA optional note
    - AC3 Rate limit on auth endpoints; CAPTCHA optional
  - Artifacts: settings, accounts/validators.py, middleware
  - Test status: [ ] pass  [ ] fail  Date: __________

- [ ] F-015 Observability and debugging
  - User story: As a developer I want actionable visibility so that I can fix issues quickly
  - Acceptance notes:
    - AC1 Structured logging with request ID; error pages customized
    - AC2 Debug toolbar only in local; email console backend verified
    - AC3 Sentry (or placeholder interface) documented for production
  - Artifacts: logging config, error templates, docs
  - Test status: [ ] pass  [ ] fail  Date: __________
