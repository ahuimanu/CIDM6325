# BRIEF: Build middleware, logging, and health slice

Goal

- Implement middleware, structured logging, and the health endpoint described in ADR-1.0.9, covering PRD §4 F-009/F-015 and §11 success metrics.

Scope (single PR)

- Files to touch: `travelmathlite/core/middleware.py`, `travelmathlite/core/views.py`, `travelmathlite/core/tests/`, `travelmathlite/urls.py`, `travelmathlite/settings.py` logging dict, `docs/ops/logging-and-health.md`.
- Non-goals: full observability stack, third-party log aggregators, UI beyond `/health/`.

Standards

- Commits: conventional style (`feat`).
- No secrets; `X-Request-ID` is header-first/UUID, logging config reads env via settings.
- Django tests: use `unittest`/`Django TestCase`; run via `manage.py test`.

Acceptance

- User flow: every request passes through middleware that adds `X-Request-ID`, structured logs include `request_id` and `duration_ms`, and `/health/` returns HTTP 200 with optional commit SHA header.
- Include migration? no.
- Update docs & PR checklist with logging sample, health curl command, invariants.

Prompts for Copilot

- "Generate middleware that records the request start time, injects `X-Request-ID` (header fallback to UUID), and logs duration before returning response."
- "Configure Django `LOGGING` dictConfig to emit JSON lines with `timestamp`, `level`, `module`, `request_id`, and `duration_ms`."
"Add a `/health/` view that returns 200, includes commit SHA header when `LOG_COMMIT_SHA` is set, and test it with Django `TestCase`."
