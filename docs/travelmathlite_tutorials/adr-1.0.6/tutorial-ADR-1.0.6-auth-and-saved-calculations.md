# Tutorial: ADR-1.0.6 Authentication and Saved Calculations

## Goal

Teach how TravelMathLite adds user authentication and a per‑user Saved Calculation history with privacy and storage limits. You will wire up auth templates, define the `SavedCalculation` model with pruning, migrate anonymous session data on login, expose list/delete views, and validate invariants with tests.

## Context and Traceability

- ADR: `docs/travelmathlite/adr/adr-1.0.6-auth-and-saved-calculations-model.md`
- Briefs: `docs/travelmathlite/briefs/adr-1.0.6/`
  - 01 Auth views/templates
  - 02 SavedCalculation model/admin
  - 03 Session migration post‑login
  - 04 Saved list/delete views
  - 05 Tests and invariants
- Apps: `travelmathlite/apps/accounts/`, `travelmathlite/apps/trips/`, `travelmathlite/core/`
- PRD Requirements: §4 F‑006 (Saved calculations), §7 NF‑003 (privacy/invariants)
- Invariants: INV‑1 privacy (users only see their own data), INV‑2 cap (max 10 saved calculations per user)

## Prerequisites

- Python 3.13+ env with `uv` and dependencies installed
- Django project configured (see earlier ADR tutorials), DB migrated
- Working calculators (distance, cost) so there is activity to save
- Bootstrap 5 in `base.html` and Django auth enabled

Quick sanity check:

```bash
cd travelmathlite
uv run python manage.py migrate
uv run python manage.py runserver
```

---

## Section 1 — Auth Views and Templates (Brief 01)

### Brief Objective

Provide signup/login/logout pages and routes using Django auth, styled via the site base template.

### Concepts (Django)

- Auth comes with built‑in views and forms you can wire into your URLs.
- Templates under `registration/` are auto‑discovered by Django auth for login/logout.

Docs: Django authentication framework (overview), authentication views, and `UserCreationForm`.

### Implementation

- URLs: `travelmathlite/apps/accounts/urls.py` wires `login`, `logout`, and a simple `SignupView`.
- Templates: `travelmathlite/apps/accounts/templates/registration/{login,logout,signup}.html` extend `base.html` and render the forms.
- Settings: `travelmathlite/core/settings.py` includes sensible `LOGIN_REDIRECT_URL` and `LOGOUT_REDIRECT_URL`.

### Verify

```bash
uv run python manage.py runserver
# Visit /accounts/login/ and /accounts/signup/
```

- Login renders and authenticates
- Signup creates a user and redirects

---

## Section 2 — SavedCalculation Model and Admin (Brief 02)

### Brief Objective

Create `SavedCalculation` to store per‑user calculator inputs/results and enforce a per‑user cap of 10 entries.

### Concepts (Django)

- Models and managers: override `save()` for local invariants.
- Admin registration for quick inspection.

### Implementation

- Model: `travelmathlite/apps/trips/models.py` defines `SavedCalculation(user, calculator_type, inputs_json, results_json, created_at)`.
- Pruning: `save()` trims oldest rows to keep at most 10 per user per calculator type.
- Admin: `travelmathlite/apps/trips/admin.py` registers model with list filters and search.

Example creation snippet (from tests):

```python
SavedCalculation.objects.create(
    user=user,
    calculator_type="distance",
    inputs_json={"origin": "JFK", "destination": "CDG"},
    results_json={"flight": 5836.0},
)
```

### Verify

```bash
uv run python manage.py shell
# create >10 entries for a user/type and confirm only 10 remain
```

Or run model tests (see Section 5).

---

## Section 3 — Session Migration on Login (Brief 03)

### Brief Objective

When a user logs in, mark the existing anonymous session as user‑bound so subsequent calculator submissions save for the user.

### Concepts (Django)

- Signals: `user_logged_in` is emitted after authentication.
- Sessions: `request.session` is available with `SessionMiddleware`.

### Implementation

- Utility: `travelmathlite/core/session.py` provides helpers like `mark_session_as_user_bound()` and `get_all_calculator_inputs()`.
- Signal: `travelmathlite/apps/accounts/signals.py` registers a receiver for `user_logged_in` that calls `mark_session_as_user_bound(request)`.
- AppConfig connects signals in `apps.py`.

### Verify

- Log in and ensure new calculator submissions save for the logged‑in user.
- Automated verification in Section 5 tests (session migration tests).

---

## Section 4 — Saved List and Delete Views (Brief 04)

### Brief Objective

Expose a list page showing a user’s saved calculations and allow deleting one.

### Concepts (Django)

- CBVs: `ListView`, `DeleteView`, plus `LoginRequiredMixin` for protection.
- Queryset scoping in `get_queryset()` to enforce INV‑1 privacy.

### Implementation

- URLs: `travelmathlite/apps/trips/urls.py` defines `saved/` and `saved/<pk>/delete/`.
- Views: `travelmathlite/apps/trips/views.py`
  - `SavedCalculationListView` — filters to `request.user` and orders by `-created_at`.
  - `SavedCalculationDeleteView` — restricts queryset to `request.user` and redirects back to list.
- Templates: `travelmathlite/apps/trips/templates/trips/{saved_list.html,saved_confirm_delete.html}` use Bootstrap tables and confirm modal/page.

### Verify

```bash
uv run python manage.py runserver
# Login, visit /trips/saved/; create some calculator runs and confirm appearance
```

- Only your records appear
- Delete removes your record and redirects

---

## Section 5 — Tests and Invariants (Brief 05)

### Brief Objective

Prove INV‑1 and INV‑2 via a comprehensive test suite: model pruning, session migration safety, and per‑user access control.

### Concepts (Django)

- `TestCase` with built‑in client and fixtures
- URL reversing and template assertions

### Implementation (files)

- `travelmathlite/apps/trips/tests/test_saved_calculation.py` — model CRUD and pruning to max 10
- `travelmathlite/apps/accounts/tests/test_session_migration.py` — signal marks session as user‑bound, idempotent behavior
- `travelmathlite/apps/trips/tests/test_views_saved.py` — list/delete access control, owner vs non‑owner

Run all tests:

```bash
cd travelmathlite
uv run python manage.py test
```

Expected:

- All tests pass
- Privacy and pruning invariants validated

---

## How It Fits Together

- Anonymous users can experiment; upon login, session becomes user‑bound.
- Subsequent valid calculator runs save as `SavedCalculation` for that user.
- Users can review and prune their history; app prunes to the newest 10 automatically.
- Tests ensure privacy (no cross‑user access) and storage limits are upheld.

## Troubleshooting

- Import resolution for `core.session`: If your type checker flags it, ensure editor/pyright are configured to treat `travelmathlite/` as an import root (see repo’s `pyrightconfig.json` and `.vscode/settings.json`).
- `HttpRequest.session` typing warnings: Safe to use with Django’s `SessionMiddleware`; suppress with targeted type‑ignore if needed.
- Test discovery conflicts: Prefer `tests/` packages over `tests.py` modules inside apps.

## References

- Django docs: Authentication, Class‑Based Views, Signals, Sessions, Testing
- Matt Layman, Understand Django: Forms, Views, Authentication, Testing (concept summaries)
- Bootstrap 5: Layout, Tables, Forms

## Next Steps

- Extend Saved Calculations UI with detail view and export (CSV/JSON)
- Add pagination/sorting to the list page
- Add user settings for per‑user cap (if requirements evolve)
