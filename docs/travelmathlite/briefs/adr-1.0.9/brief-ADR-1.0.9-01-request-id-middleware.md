# BRIEF: Build request ID + timing middleware

Goal

- Implement middleware that injects `X-Request-ID`, records request duration, and exposes values for logging (PRD §4 F-009, NF-004).

Scope (single PR)

- Files to touch: `travelmathlite/core/middleware.py`, `travelmathlite/settings.py` (MIDDLEWARE list), `travelmathlite/core/tests/test_middleware.py`.
- Non-goals: external tracing services, instrumentation beyond duration header.

Standards

- Commits: conventional style (`feat`).
- No secrets; `request_id` derived from `X-Request-ID` header (if present) or UUID4.
- Django tests: use `unittest.TestCase` or Django `TestCase`; run via `uv run python manage.py test travelmathlite.core.tests`.

Acceptance

- Every incoming request gets `X-Request-ID` header (echoed on response) and stores start time for logging.
- Middleware exposes `request.request_id` and `request.duration_ms` accessible to loggers.
- Include invariants: INV-1 (request ID always present), INV-2 (duration logged even on exceptions).
- Include migration? no.
- Update docs/PR checklist to cite how to verify request IDs and durations.

Prompts for Copilot

- "Generate Django middleware that reads `X-Request-ID` from headers or generates a UUID, attaches it to the request/response, and records start/end timestamps."
"Ensure middleware stores duration in milliseconds and survives exceptions so logging can always access `request.duration_ms`."
