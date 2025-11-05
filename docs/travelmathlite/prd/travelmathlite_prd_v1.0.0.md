# Product Requirements Document

> How to use this document
>
> - This PRD follows the template in `docs/travelmathlite/adr/prd_template_v1.0.1.md`
> - Headings and section order are preserved; guidance text removed
> - This plan targets a Django + Bootstrap 5 + HTMX clone of <https://www.travelmath.com/> named "travelmathlite"
> - Scope intentionally covers the full arc of "Understand Django" chapters

## 1. Document information

- Product or feature name: travelmathlite
- Author(s): Course Staff
- Date created: 2025-11-02
- Last updated: 2025-11-02
- Version: 1.0.0 draft

---

## 2. Overview

- Summary: travelmathlite is a learning-oriented clone of Travelmath that calculates travel distances, driving times and costs, flight distances, nearest airports, and simple trip plans. It is built with Django, vanilla Bootstrap 5, and the latest HTMX to demonstrate full-stack Django techniques from URLs to deployment.
- Problem statement: Learners need a realistic, end-to-end Django project that exercises all core topics while producing a useful travel calculator experience.
- Goals and objectives:
  - Provide distance and time calculators across cities, airports, and coordinates
  - Offer nearest airport lookup and basic trip planning
  - Deliver responsive UI with Bootstrap 5 and progressive enhancement via HTMX
  - Exercise all key Django concepts: URLs, views, templates, forms, models, admin, auth, middleware, static, testing, deployment, sessions, settings, media, commands, performance, security, debugging
- Non-goals:
  - Real-time traffic routing or live map tiles
  - Airline ticketing or booking flows
  - Complex GIS stack; we’ll use haversine/approximate calculations

---

## 3. Context and background

- Business context: Teaching tool for CIDM 6325 to practice production-minded Django skills
- Market or customer insights: Students want hands-on projects that feel real and demonstrate job-ready features
- Competitive or benchmark references: <https://www.travelmath.com/> for feature inspiration

---

## 4. Scope items and checklist seeds

> Capabilities are checklistable units with IDs and testable acceptance notes.

- [ ] **F-001 Distance calculator (city/airport/coord)**  
  User story As a traveler I want to compute distance and driving time between two places so that I can plan a trip  
  Acceptance notes
  - AC1 Support input by city name, airport code, or lat/long
  - AC2 Show driving distance/time and straight-line (flight) distance
  - AC3 HTMX submit updates results without full page reload; progressive enhancement preserves full form POST/GET
  - AC4 Persist last inputs in session for quick repeat
  Artifacts `apps/calculators/`, `templates/calculators/`, `calculators/views.py`, `forms.py`  
  Owner Team  Target version 0.1

- [ ] **F-002 Nearest airport lookup**  
  User story As a traveler I want the nearest airport to a city or coordinate so that I can choose flights  
  Acceptance notes
  - AC1 Input city or coordinates return nearest airport with distance
  - AC2 Show a short list of top 3 airports sorted by distance
  - AC3 Link to airport detail page
  Artifacts `apps/airports/`, `airports/views.py`, `templates/airports/`  
  Owner Team  Target version 0.1

- [ ] **F-003 Cost of driving estimator**  
  User story As a traveler I want an estimated fuel cost so that I can budget  
  Acceptance notes
  - AC1 Inputs: distance (km/mi), fuel economy, fuel price
  - AC2 Defaults via settings; override per request via HTMX
  - AC3 Currency and units displayed consistently; form validation errors shown
  Artifacts `calculators/costs.py`, `calculators/forms.py`, `templates/calculators/partials/`  
  Owner Team  Target version 0.1

- [ ] **F-004 Place and airport data models**  
  User story As a developer I want normalized models so that queries are fast and maintainable  
  Acceptance notes
  - AC1 Models: City, Airport, Country with indexes on lookups
  - AC2 Custom manager for published/active records and case-insensitive search
  - AC3 Admin: list_display, search_fields, list_filter; CSV import action
  Artifacts `apps/core/models.py`, `apps/airports/models.py`, admin configs, `migrations/`  
  Owner Team  Target version 0.1

- [ ] **F-005 Data import command**  
  User story As an operator I want a command to load seed datasets so that the app is usable  
  Acceptance notes
  - AC1 Management command `import_airports` idempotent with `--dry-run`
  - AC2 Logs progress and handles retries; validates row counts
  - AC3 Supports file path argument and remote URL
  Artifacts `apps/airports/management/commands/import_airports.py`  
  Owner Team  Target version 0.1

- [ ] **F-006 Accounts and saved trips**  
  User story As a user I want to save recent calculations so that I can reuse them  
  Acceptance notes
  - AC1 Auth: login/logout, registration; use Django auth views
  - AC2 Save last 10 calculations per user; list and delete
  - AC3 Session remembers last anonymous inputs; migrate on login
  Artifacts `apps/accounts/`, `apps/trips/`, `templates/accounts/`, `templates/trips/`  
  Owner Team  Target version 0.2

- [ ] **F-007 Site navigation, layout, and branding**  
  User story As a user I want a clean responsive UI so that I can use the app on any device  
  Acceptance notes
  - AC1 Base template with Bootstrap 5; navbar, footer; sticky footer
  - AC2 Static assets via collectstatic; favicon, CSS bundle
  - AC3 Accessibility: color contrast, focus states, ARIA on forms
  Artifacts `templates/base.html`, `templates/includes/`, `static/`  
  Owner Team  Target version 0.1

- [ ] **F-008 Search and URL design**  
  User story As a user I want friendly URLs and search so that pages are shareable and discoverable  
  Acceptance notes
  - AC1 Namespaced URLs with reversing everywhere
  - AC2 Search cities/airports by name/code with pagination; highlight results
  - AC3 Robots, sitemap, canonical links for key pages
  Artifacts `urls.py`, `apps/search/views.py`, `templates/search/`  
  Owner Team  Target version 0.2

- [ ] **F-009 Middleware and request tracing**  
  User story As an operator I want timing and correlation IDs so that I can debug issues  
  Acceptance notes
  - AC1 Custom middleware adds `X-Request-ID` and logs duration
  - AC2 Security and common middleware configured; GZip or ConditionalGet
  - AC3 Health endpoint returns OK with commit SHA
  Artifacts `core/middleware.py`, settings, `urls.py`  
  Owner Team  Target version 0.2

- [ ] **F-010 Static and media management**  
  User story As an operator I want reliable static and media handling so that deploys are stable  
  Acceptance notes
  - AC1 STATICFILES_DIRS and app static organized; collectstatic required
  - AC2 ManifestStaticFilesStorage enabled in prod
  - AC3 MEDIA configured; optional user avatar upload on profile
  Artifacts settings, `static/`, `media/`, `accounts/forms.py`  
  Owner Team  Target version 0.2

- [ ] **F-011 Testing and CI signals**  
  User story As a developer I want confidence in changes so that regressions are caught  
  Acceptance notes
  - AC1 Django TestCase coverage for calculators, search, and auth flows
  - AC2 RequestFactory and assertTemplateUsed employed
  - AC3 Mock external calls; deterministically freeze time in tests
  Artifacts `apps/*/tests.py`, coverage report, CI config  
  Owner Team  Target version 0.2

- [ ] **F-012 Deployment-ready settings**  
  User story As an operator I want safe defaults so that production is secure  
  Acceptance notes
  - AC1 Split settings: base/local/prod; DEBUG=False in prod; ALLOWED_HOSTS set
  - AC2 Env var parsing via `django-environ` and secrets sourced securely
  - AC3 Security headers configured; HTTPS ready
  Artifacts `project/settings/{base,local,prod}.py`  
  Owner Team  Target version 0.3

- [ ] **F-013 Performance and caching**  
  User story As a user I want fast responses so that the app feels snappy  
  Acceptance notes
  - AC1 Use select_related/prefetch_related and indexes on hot paths
  - AC2 Enable per-view/low-level caching on search and airport endpoints
  - AC3 Cache headers for static/dynamic responses as appropriate
  Artifacts code annotations, settings caches, middleware  
  Owner Team  Target version 0.3

- [ ] **F-014 Security posture**  
  User story As an operator I want common risks mitigated so that user data is protected  
  Acceptance notes
  - AC1 CSRF and input sanitization verified; templates autoescape; bleach where needed
  - AC2 Auth hardening with validators; admin access restricted; 2FA optional note
  - AC3 Rate limit on auth endpoints; CAPTCHA optional
  Artifacts settings, `accounts/validators.py`, middleware  
  Owner Team  Target version 0.3

- [ ] **F-015 Observability and debugging**  
  User story As a developer I want actionable visibility so that I can fix issues quickly  
  Acceptance notes
  - AC1 Structured logging with request ID; error pages customized
  - AC2 Debug toolbar only in local; email console backend verified
  - AC3 Sentry (or placeholder interface) documented for production
  Artifacts logging config, error templates, docs  
  Owner Team  Target version 0.3

### Out of scope

- Real-time navigation turn-by-turn
- Payments and reservations
- Vendor integrations beyond simple dataset imports

---

## 5. Functional requirements bound to scope

- **FR-F-001-1** Compute driving and straight-line distance between two places  
  Rationale travel planning core  
  Trace F-001
- **FR-F-001-2** Validate and normalize inputs (city, airport code, lat/long)  
  Rationale data quality  
  Trace F-001
- **FR-F-002-1** Return nearest airport with accurate ranking  
  Rationale flight planning  
  Trace F-002
- **FR-F-003-1** Estimate fuel cost with configurable defaults  
  Rationale budgeting  
  Trace F-003
- **FR-F-004-1** Provide models and admin with search/filter  
  Rationale maintainability  
  Trace F-004
- **FR-F-005-1** Import airports dataset idempotently  
  Rationale operability  
  Trace F-005
- **FR-F-006-1** Save last 10 calculations per user  
  Rationale convenience  
  Trace F-006
- **FR-F-007-1** Deliver responsive pages with Bootstrap  
  Rationale accessibility  
  Trace F-007
- **FR-F-008-1** Search with pagination and highlighting  
  Rationale discoverability  
  Trace F-008
- **FR-F-009-1** Add request ID and duration to logs  
  Rationale traceability  
  Trace F-009
- **FR-F-010-1** Configure static/media with hashed filenames  
  Rationale cache safety  
  Trace F-010
- **FR-F-011-1** Cover critical flows with TestCase  
  Rationale quality  
  Trace F-011
- **FR-F-012-1** Split settings and secure prod defaults  
  Rationale safety  
  Trace F-012
- **FR-F-013-1** Optimize queries and cache hot endpoints  
  Rationale speed  
  Trace F-013
- **FR-F-014-1** Harden auth and rate-limit sensitive endpoints  
  Rationale security  
  Trace F-014
- **FR-F-015-1** Provide structured logs and error pages  
  Rationale supportability  
  Trace F-015

---

## 6. Checklist to be generated from scope

At sign off, generate a one-page checklist from section 4 into `docs/checklists/travelmathlite_feature_checklist.md` with boxes, user stories, acceptance notes, artifact links, and a test status flag.

---

## 7. Non functional requirements

- **NF-001 Performance** P95 < 300 ms for simple lookups; < 700 ms for compute-heavy endpoints; verified via local profiling and log timings
- **NF-002 Accessibility** WCAG AA color contrast; keyboard navigability; verify with axe DevTools and manual checks
- **NF-003 Security** CSRF enabled, HTTPS-ready, secure cookies, password validators; verify via settings inspection and automated tests
- **NF-004 Reliability** Health check endpoint returns 200; management command idempotent; basic backup/restore plan for DB

---

## 8. Dependencies

- Internal: core, calculators, airports, accounts, trips apps
- External: seed datasets (open airports/cities); optional Sentry account; email SMTP for password reset
- Cross team: none

---

## 9. Risks and assumptions

- Dataset quality varies; mitigation include validation and fallbacks
- No real-time traffic or routing APIs; distances approximate
- Students have local dev environment per course setup

---

## 10. Acceptance criteria

- Distance, nearest airport, and cost calculators return results with valid inputs and handle errors gracefully
- Search paginates and highlights, with canonical URLs and sitemap included
- Auth flows work; sessions store last anonymous inputs; saved trips list works
- Static and media configured; collectstatic and hashed filenames in prod settings
- Tests cover calculators, search, auth flows; CI or local equivalent run; coverage reported

---

## 11. Success metrics

- 100% of scope F-### items done with passing tests and artifacts linked
- P95 latency targets met locally on sample data; profiling checked in
- Accessibility checks pass; no critical security misconfigurations in settings

---

## 12. Rollout and release plan

- MVP 0.1: F-001, F-002, F-003, F-004, F-005, F-007
- 0.2: F-006, F-008, F-009, F-010, F-011
- 0.3: F-012, F-013, F-014, F-015
- Releases: staged to local, then demo server if available; docs and a quick start in README

---

## 13. Traceability

- F-001 → FR-F-001-1 FR-F-001-2 → tests T-001a T-001b → `calculators/views.py`, `templates/calculators/`
- F-002 → FR-F-002-1 → tests T-002a → `airports/views.py`, `templates/airports/`
- F-003 → FR-F-003-1 → tests T-003a → `calculators/forms.py`, `templates/calculators/partials/`
- F-004 → FR-F-004-1 → tests T-004a → `core/models.py`, admin configs
- F-005 → FR-F-005-1 → tests T-005a → `management/commands/import_airports.py`
- F-006 → FR-F-006-1 → tests T-006a → `trips/views.py`, `templates/trips/`
- F-007 → FR-F-007-1 → tests T-007a → `templates/base.html`, `static/`
- F-008 → FR-F-008-1 → tests T-008a → `search/views.py`, `templates/search/`
- F-009 → FR-F-009-1 → tests T-009a → `core/middleware.py`
- F-010 → FR-F-010-1 → tests T-010a → `settings.py`, `static/`, `media/`
- F-011 → FR-F-011-1 → tests T-011a → `apps/*/tests.py`
- F-012 → FR-F-012-1 → tests T-012a → `settings/`
- F-013 → FR-F-013-1 → tests T-013a → code annotations, cache configs
- F-014 → FR-F-014-1 → tests T-014a → `accounts/`, middleware
- F-015 → FR-F-015-1 → tests T-015a → logging config, error templates

---

## 14. Open questions

- Which airport dataset source to standardize on (OpenFlights vs. OurAirports)
- Is a public demo environment available or local-only
- Whether to include time zone conversions in MVP

---

## 15. References

- Template `docs/travelmathlite/adr/prd_template_v1.0.1.md`
- Benchmark <https://www.travelmath.com/>
- Django book <https://www.mattlayman.com/understand-django/>

---

## Appendix A Chapter coverage

This appendix maps chapters from "Understand Django" to travelmathlite features (F-###) and key
acceptance notes, to simplify audit of coverage.

- Chapter 1 From Browser To Django
  - F-009 Middleware and request tracing (AC1 request ID, duration), F-008 URL design
  - Emphasis: request/response lifecycle is exercised end-to-end across calculators and search
- Chapter 2 URLs Lead The Way
  - F-008 Search and URL design (AC1 namespaced reversing), F-007 navbar links
- Chapter 3 Views On Views
  - F-001, F-002, F-003, F-006, F-008 implement class-based views and FBV where appropriate
- Chapter 4 Templates For User Interfaces
  - F-007 base/partials with Bootstrap 5; F-008 highlights and pagination templates
- Chapter 5 User Interaction With Forms
  - F-001, F-003 calculators use forms; validation and CSRF; HTMX progressive enhancement
- Chapter 6 Store Data With Models
  - F-004 models (City/Airport/Country), managers, indexes; F-006 saved calculations
- Chapter 7 Administer All The Things
  - F-004 admin config (list_display, search_fields, list_filter) and CSV import action
- Chapter 8 Anatomy Of An Application
  - App layout `apps/*`, per-app urls/templates/static reflected across all features
- Chapter 9 User Authentication
  - F-006 accounts flows; F-014 auth validators and admin access restrictions
- Chapter 10 Middleware Do You Go
  - F-009 custom middleware; built-ins like SecurityMiddleware, GZip/ConditionalGet configured
- Chapter 11 Serving Static Files
  - F-007 static assets; F-010 STATICFILES_DIRS and ManifestStaticFilesStorage
- Chapter 12 Test Your Apps
  - F-011 TestCase coverage, RequestFactory, assertTemplateUsed, mocking, time freeze
- Chapter 13 Deploy A Site Live
  - F-012 split settings, DEBUG=False, ALLOWED_HOSTS; security headers; rollout plan in Section 12
- Chapter 14 Per-visitor Data With Sessions
  - F-001 AC4 session persistence; F-006 session migration on login
- Chapter 15 Making Sense Of Settings
  - F-012 env parsing with django-environ; secrets handling; base/local/prod
- Chapter 16 User File Use
  - F-010 optional avatar upload; MEDIA configured
- Chapter 17 Command Your App
  - F-005 `import_airports` management command with --dry-run and idempotency
- Chapter 18 Go Fast With Django
  - F-013 query optimization (select_related/prefetch_related), indexes, caching
- Chapter 19 Security And Django
  - F-014 CSRF, input sanitization, validators, rate limiting/CAPTCHA
- Chapter 20 Debugging Tips And Techniques
  - F-015 structured logs, error pages, local debug toolbar; Sentry documented
