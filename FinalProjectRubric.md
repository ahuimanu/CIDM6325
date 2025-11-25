# Guide to Book Topics for Final Project (Baseline, Good, Better, Best)

***NOTE***: Updated 11/02/2025
Finalized for Fall 2025.  

***NOTE***: You **MUST** document and identify which of the Good, Better, Best features you are using in your project in your project's readme.

## Example: How to score your project

Here’s a concrete example of a passing selection. Baseline items are assumed completed across chapters. The student then selects from Good/Better/Best to meet the targets:

- Good (pick at least 4)
  - URLs: Named URLs & reversing (`reverse`, `{% url %}`)
  - Views: Intro to CBVs and Generic CBVs (e.g., `ListView`, `DetailView`)
  - Templates: Inheritance with `{% extends %}` and `{% block %}` + `{% include %}` partials
  - Forms: `FormView` with success redirect and CSRF
- Better (pick at least 2)
  - Templates: Custom tag/filter (e.g., a safe highlight filter) and built-in helpers
  - Forms/CRUD: `ModelForm` mapping 1:1 to a model
- Best (pick at least 1)
  - Performance/Security/Deploy: Add simple caching for a list view, or observability (basic logs/health check), or HTTPS-secure settings

This example satisfies: 4× Good, 2× Better, 1× Best, plus all Baseline. You can mix chapters—choose items that serve your app’s goals.

## How to use this List

I have classified the learning objectives from [Matt's book](https://www.mattlayman.com/understand-django/browser-to-django/) according to the following scheme. Each category is relative to the following requirements for your final project:

- You must implement *all* **Baseline** components - Gets you to 70% of the value
- You will implement *at least* four **Good** components - Gets you to 80% of the value
- You will implement *at least* two **Better** components - Gets you to 85% of the value
- You will implement *at least* one **Best** component - Gets you to 90% of the value

Where is the remaining 10%? It comes from the synthesis and service to your implementation approach.

- **Baseline** 🟩: Essential Django knowledge that must be demonstrated in your final project  
- **Good** 🟨: Fundamental knowledge that sets up a more useful app  
- **Better** 🟧: Approaching a higher degree of robustness  
- **Best** 🟥: Approaching professional-grade features and tools

NOTE: The chapter references indicate where a technique is introduced. Demonstrate the technique in your project—you need not mirror the exact example from the text.

---

Topic | Baseline 🟩 | Good 🟨 | Better 🟧 | Best 🟥
---|---|---|---|---
***[Chapter 1 — From Browser To Django](https://www.mattlayman.com/understand-django/browser-to-django/)*** | - | - | - | -
[Web request/response lifecycle](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[DNS → IP → HTTP (context)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[HTTP methods & headers](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[WSGI (where HTTP meets Python)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[Django’s job: URLs + views](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
[Getting Django set up (venv, startproject)](https://www.mattlayman.com/understand-django/browser-to-django/) | 🟩 | - | - | -
***[Chapter 2 — URLs Lead The Way](https://www.mattlayman.com/understand-django/urls-lead-way/)*** | - | - | - | -
[URLconf basics: `path()`/`urlpatterns`](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[Route converters (`<int:>`, `<slug:>`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[Ordering/specificity of patterns](https://www.mattlayman.com/understand-django/urls-lead-way/) | 🟩 | - | - | -
[`include()` and namespacing (`app_name`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | 🟨 | - | -
[Named URLs & reversing (`reverse`, `{% url %}`)](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | 🟨 | - | -
[`re_path()` and regex routes](https://www.mattlayman.com/understand-django/urls-lead-way/) | - | - | 🟧 | -
***[Chapter 3 — Views On Views](https://www.mattlayman.com/understand-django/views-on-views/)*** | - | - | - | -
[Function-Based Views (FBV)](https://www.mattlayman.com/understand-django/views-on-views/) | 🟩 | - | - | -
[`HttpRequest`/`HttpResponse` essentials](https://www.mattlayman.com/understand-django/views-on-views/) | 🟩 | - | - | -
[Intro to Class-Based Views (CBV)](https://www.mattlayman.com/understand-django/views-on-views/) | - | 🟨 | - | -
[Generic CBVs (`TemplateView`, etc.)](https://www.mattlayman.com/understand-django/views-on-views/) | - | 🟨 | - | -
[View decorators (auth, cache, etc.)](https://www.mattlayman.com/understand-django/views-on-views/) | - | - | 🟧 | -
[Organizing view code for clarity](https://www.mattlayman.com/understand-django/views-on-views/) | - | - | 🟧 | -
***[Chapter 4 — Templates For User Interfaces](https://www.mattlayman.com/understand-django/templates-user-interfaces/)*** | - | - | - | -
[`TEMPLATES` settings & loaders](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | 🟩 | - | - | -
[Rendering from views (`render`, CBV context)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | 🟩 | - | - | -
[DTL variables, filters, tags](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[Inheritance: `{% extends %}`, `{% block %}`](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[`{% include %}` and partials](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | 🟨 | - | -
[Custom tags/filters (`templatetags/`)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | - | 🟧 | -
[Built-in helpers (`url`, `spaceless`, etc.)](https://www.mattlayman.com/understand-django/templates-user-interfaces/) | - | - | 🟧 | -
***[Chapter 5 — User Interaction With Forms](https://www.mattlayman.com/understand-django/user-interaction-forms/)*** | - | - | - | -
[`Form classes: fields → HTML`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | 🟩 | - | - | -
[GET vs POST, bound forms, `is_valid()`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | 🟩 | - | - | -
[CSRF & `{% csrf_token %}`](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | 🟨 | - | -
[`FormView` / success redirect](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | 🟨 | - | -
[Common widgets & validation patterns](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - |  | - | -
[ModelForms for CRUD](https://www.mattlayman.com/understand-django/user-interaction-forms/) | - | - | 🟧 | -
***[Chapter 6 — Store Data With Models](https://www.mattlayman.com/understand-django/store-data-with-models/)*** | - | - | - | -
[Define models and fields](https://www.mattlayman.com/understand-django/store-data-with-models/) | 🟩 | - | - | -
[Migrations (`makemigrations`/`migrate`)](https://www.mattlayman.com/understand-django/store-data-with-models/) | 🟩 | - | - | -
[QuerySets: filter/order/limit](https://www.mattlayman.com/understand-django/store-data-with-models/) | - | 🟨 | - | -
[Relationships (FK/M2M/OneToOne)](https://www.mattlayman.com/understand-django/store-data-with-models/) | - | 🟨 | - | -
[Custom managers/QuerySet methods](https://www.mattlayman.com/understand-django/store-data-with-models/) | - | - | 🟧 | -
[Aggregation/annotations](https://www.mattlayman.com/understand-django/store-data-with-models/) | - | - | 🟧 | -
***[Chapter 7 — Administer All The Things](https://www.mattlayman.com/understand-django/administer-all-the-things/)*** | - | - | - | -
[Enable admin and register models](https://www.mattlayman.com/understand-django/administer-all-the-things/) | 🟩 | - | - | -
[ModelAdmin list/search/filter](https://www.mattlayman.com/understand-django/administer-all-the-things/) | - | 🟨 | - | -
[Inlines and fieldsets](https://www.mattlayman.com/understand-django/administer-all-the-things/) | - | - | 🟧 | -
[Custom actions/export](https://www.mattlayman.com/understand-django/administer-all-the-things/) | - | - | 🟧 | -
[Template overrides/theming](https://www.mattlayman.com/understand-django/administer-all-the-things/) | - | - | - | 🟥
***[Chapter 8 — Anatomy Of An Application](https://www.mattlayman.com/understand-django/anatomy-of-an-application/)*** | - | - | - | -
[App config and structure](https://www.mattlayman.com/understand-django/anatomy-of-an-application/) | 🟩 | - | - | -
[URLs/templates/static per app](https://www.mattlayman.com/understand-django/anatomy-of-an-application/) | - | 🟨 | - | -
[Reusable app boundaries](https://www.mattlayman.com/understand-django/anatomy-of-an-application/) | - | - | 🟧 | -
[Signals/wiring within app](https://www.mattlayman.com/understand-django/anatomy-of-an-application/) | - | - | 🟧 | -
[Packaging/releasing an app](https://www.mattlayman.com/understand-django/anatomy-of-an-application/) | - | - | - | 🟥
***[Chapter 9 — User Authentication](https://www.mattlayman.com/understand-django/user-authentication/)*** | - | - | - | -
[Login/logout flow](https://www.mattlayman.com/understand-django/user-authentication/) | 🟩 | - | - | -
[User model access (`get_user_model`)](https://www.mattlayman.com/understand-django/user-authentication/) | - | 🟨 | - | -
[Permissions/authorization checks](https://www.mattlayman.com/understand-django/user-authentication/) | - | 🟨 | 🟧 | -
[Password reset/change emails](https://www.mattlayman.com/understand-django/user-authentication/) | - | - | 🟧 | -
[SSO/social auth integration](https://www.mattlayman.com/understand-django/user-authentication/) | - | - | - | 🟥
***[Chapter 10 — Middleware Do You Go?](https://www.mattlayman.com/understand-django/middleware-do-you-go/)*** | - | - | - | -
[What middleware is and order](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | 🟩 | - | - | -
[Use key built-ins (Security, CSRF)](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | 🟨 | - | -
[Write a small custom middleware](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | - | 🟧 | -
[Measure/optimize impact](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | - | - | 🟥
[GZip/ConditionalGet built-ins](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | 🟨 | - | -
[Messages/Auth/Session wiring](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | 🟨 | - | -
[Correlation IDs/metrics via middleware](https://www.mattlayman.com/understand-django/middleware-do-you-go/) | - | - | - | 🟥
***[Chapter 11 — Serving Static Files](https://www.mattlayman.com/understand-django/serving-static-files/)*** | - | - | - | -
[STATIC_URL and finders](https://www.mattlayman.com/understand-django/serving-static-files/) | 🟩 | - | - | -
[collectstatic for deploy](https://www.mattlayman.com/understand-django/serving-static-files/) | - | 🟨 | - | -
[Whitenoise (no CDN) setup](https://www.mattlayman.com/understand-django/serving-static-files/) | - | - | 🟧 | -
[CDN integration/versioning](https://www.mattlayman.com/understand-django/serving-static-files/) | - | - | - | 🟥
[STATICFILES_DIRS vs app static](https://www.mattlayman.com/understand-django/serving-static-files/) | - | 🟨 | - | -
[ManifestStaticFilesStorage (hash names)](https://www.mattlayman.com/understand-django/serving-static-files/) | - | - | 🟧 | -
***[Chapter 12 — Test Your Apps](https://www.mattlayman.com/understand-django/test-your-apps/)*** | - | - | - | -
[Django TestCase basics](https://www.mattlayman.com/understand-django/test-your-apps/) | 🟩 | - | - | -
[Client + URL reversing in tests](https://www.mattlayman.com/understand-django/test-your-apps/) | - | 🟨 | - | -
[Factories/fixtures, coverage](https://www.mattlayman.com/understand-django/test-your-apps/) | - | - | 🟧 | -
[CI pipeline/test matrix](https://www.mattlayman.com/understand-django/test-your-apps/) | - | - | - | 🟥
[RequestFactory, assertTemplateUsed](https://www.mattlayman.com/understand-django/test-your-apps/) | - | 🟨 | - | -
[Mock external services; freeze time](https://www.mattlayman.com/understand-django/test-your-apps/) | - | - | 🟧 | -
[Parallel tests; isolate flakiness](https://www.mattlayman.com/understand-django/test-your-apps/) | - | - | - | 🟥
***[Chapter 13 — Deploy A Site Live](https://www.mattlayman.com/understand-django/deploy-site-live/)*** | - | - | - | -
[Env vars and secret settings](https://www.mattlayman.com/understand-django/deploy-site-live/) | 🟩 | - | - | -
[Database provisioning/migrations](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | 🟨 | - | -
[App server + proxy (Gunicorn/Nginx)](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | - | 🟧 | -
[Observability (logs, health checks)](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | - | 🟧 | -
[Infra as Code and blue/green](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | - | - | 🟥
[DEBUG=False, ALLOWED_HOSTS hygiene](https://www.mattlayman.com/understand-django/deploy-site-live/) | 🟩 | - | - | -
[Static/media hosting plan](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | 🟨 | - | -
[Zero-downtime migration strategy](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | - | 🟧 | -
[Rollback + post-deploy smoke tests](https://www.mattlayman.com/understand-django/deploy-site-live/) | - | - | - | 🟥
***[Chapter 14 — Per-visitor Data With Sessions](https://www.mattlayman.com/understand-django/sessions/)*** | - | - | - | -
[Use `request.session` safely](https://www.mattlayman.com/understand-django/sessions/) | 🟩 | - | - | -
[Common patterns (flash msgs, carts)](https://www.mattlayman.com/understand-django/sessions/) | - | 🟨 | - | -
[Session backends/config](https://www.mattlayman.com/understand-django/sessions/) | - | - | 🟧 | -
[Security flags/expiry policy](https://www.mattlayman.com/understand-django/sessions/) | - | - | - | 🟥
[Choose backend (DB/cached/signed cookies)](https://www.mattlayman.com/understand-django/sessions/) | - | 🟨 | - | -
[Rotate keys/serializer; audit access](https://www.mattlayman.com/understand-django/sessions/) | - | - | 🟧 | -
[Privacy: minimize PII in session](https://www.mattlayman.com/understand-django/sessions/) | - | - | - | 🟥
***[Chapter 15 — Making Sense Of Settings](https://www.mattlayman.com/understand-django/settings/)*** | - | - | - | -
[Settings and configuration](https://www.mattlayman.com/understand-django/settings/) | 🟩 | - | - | -
[Split settings by environment](https://www.mattlayman.com/understand-django/settings/) | - | 🟨 | - | -
[Use env parsing (`django-environ`)](https://www.mattlayman.com/understand-django/settings/) | - | - | 🟧 | -
[Secrets manager integration](https://www.mattlayman.com/understand-django/settings/) | - | - | - | 🟥
[12-factor .env convention](https://www.mattlayman.com/understand-django/settings/) | - | 🟨 | - | -
[Compose settings (base/local/prod)](https://www.mattlayman.com/understand-django/settings/) | - | - | 🟧 | -
[Secret rotation and reload plan](https://www.mattlayman.com/understand-django/settings/) | - | - | - | 🟥
***[Chapter 16 — User File Use](https://www.mattlayman.com/understand-django/media-files/)*** | - | - | - | -
[MEDIA_URL/ROOT and uploads](https://www.mattlayman.com/understand-django/media-files/) | 🟩 | - | - | -
[Model/FileField forms + cleanup](https://www.mattlayman.com/understand-django/media-files/) | - | 🟨 | - | -
[Validation (type/size), thumbnails](https://www.mattlayman.com/understand-django/media-files/) | - | - | 🟧 | -
[Cloud storage (S3, permissions)](https://www.mattlayman.com/understand-django/media-files/) | - | - | - | 🟥
[Admin upload UX and cleanup tasks](https://www.mattlayman.com/understand-django/media-files/) | - | 🟨 | - | -
[Antivirus/scan pipeline for uploads](https://www.mattlayman.com/understand-django/media-files/) | - | - | 🟧 | -
[Direct-to-cloud signed URL uploads](https://www.mattlayman.com/understand-django/media-files/) | - | - | - | 🟥
***[Chapter 17 — Command Your App](https://www.mattlayman.com/understand-django/command-apps/)*** | - | - | - | -
[Use built-in manage.py commands](https://www.mattlayman.com/understand-django/command-apps/) | 🟩 | - | - | -
[Write a simple custom command](https://www.mattlayman.com/understand-django/command-apps/) | - | 🟨 | - | -
[Options, logging, idempotency](https://www.mattlayman.com/understand-django/command-apps/) | - | - | 🟧 | -
[Schedule/operationalize (cron/beat)](https://www.mattlayman.com/understand-django/command-apps/) | - | - | - | 🟥
[Helpful --dry-run and help text](https://www.mattlayman.com/understand-django/command-apps/) | - | 🟨 | - | -
[Locks/retries; progress reporting](https://www.mattlayman.com/understand-django/command-apps/) | - | - | 🟧 | -
***[Chapter 18 — Go Fast With Django](https://www.mattlayman.com/understand-django/go-fast/)*** | - | - | - | -
[Paginate heavy lists](https://www.mattlayman.com/understand-django/go-fast/) | 🟩 | - | - | -
[Efficient queries (`select_related`)](https://www.mattlayman.com/understand-django/go-fast/) | - | 🟨 | - | -
[Caching (per-view/low-level)](https://www.mattlayman.com/understand-django/go-fast/) | - | - | 🟧 | -
[N+1 detection, cache invalidation](https://www.mattlayman.com/understand-django/go-fast/) | - | - | - | 🟥
[DB indexes and EXPLAIN basics](https://www.mattlayman.com/understand-django/go-fast/) | - | 🟨 | - | -
[Cache headers (ETag/Last-Modified)](https://www.mattlayman.com/understand-django/go-fast/) | - | 🟨 | - | -
[Profiling (CPU/mem); query budgets](https://www.mattlayman.com/understand-django/go-fast/) | - | - | 🟧 | -
[Read replicas/partitioning strategy](https://www.mattlayman.com/understand-django/go-fast/) | - | - | - | 🟥
***[Chapter 19 — Security And Django](https://www.mattlayman.com/understand-django/secure-apps/)*** | - | - | - | -
[CSRF, XSS, and input sanitizing](https://www.mattlayman.com/understand-django/secure-apps/) | 🟩 | - | - | -
[Auth hardening (validators)](https://www.mattlayman.com/understand-django/secure-apps/) | - | 🟨 | - | -
[HTTPS + `SECURE_*` settings](https://www.mattlayman.com/understand-django/secure-apps/) | - | - | 🟧 | -
[CSP/headers, permission strategy](https://www.mattlayman.com/understand-django/secure-apps/) | - | - | - | 🟥
[Admin hardening (limit staff, 2FA)](https://www.mattlayman.com/understand-django/secure-apps/) | - | 🟨 | - | -
[Rate limiting/CAPTCHA on auth forms](https://www.mattlayman.com/understand-django/secure-apps/) | - | - | 🟧 | -
[Secrets scanning and rotation policy](https://www.mattlayman.com/understand-django/secure-apps/) | - | - | - | 🟥
***[Chapter 20 — Debugging Tips And Techniques](https://www.mattlayman.com/understand-django/debugging-tips-techniques/)*** | - | - | - | -
[Logging and error pages](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | 🟩 | - | - | -
[Django Debug Toolbar](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | 🟨 | - | -
[Structured logs, trace IDs](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | - | 🟧 | -
[Error tracking (Sentry) + alerts](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | - | - | 🟥
[Werkzeug/Runserver Plus debugger](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | 🟨 | - | -
[Email outbox/console backend checks](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | 🟨 | - | -
[Log aggregation (ELK/CloudWatch)](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | - | 🟧 | -
[Distributed tracing (OpenTelemetry)](https://www.mattlayman.com/understand-django/debugging-tips-techniques/) | - | - | - | 🟥

### Optional 3rd Party Tools to consider

- [Django admin](https://github.com/wsvincent/awesome-django#admin)
- [APIs](https://github.com/wsvincent/awesome-django#apis)
- [Async](https://github.com/wsvincent/awesome-django#async)
- [ECommerce](https://github.com/wsvincent/awesome-django#ecommerce)
- [Files and Images](https://github.com/wsvincent/awesome-django#filesimages)
- [Model enhancements](https://github.com/wsvincent/awesome-django#models)
- [Search](https://github.com/wsvincent/awesome-django#search)
- [Tasks and Job Scheduling](https://github.com/wsvincent/awesome-django#task-queues)
- [Users and SSO](https://github.com/wsvincent/awesome-django#users)
- [Views](https://github.com/wsvincent/awesome-django#views)

***NOTE A***: This does not JUST mean in the inclusion of any [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).  I would strongly recommend [htmx](https://htmx.org/) if you need any front-end JS magic. However, it should be the case that MOST JavaScript is optional.

---
