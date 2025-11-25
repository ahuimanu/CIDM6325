# BRIEF: Build health endpoint

Goal

- Implement `/health/` view that returns HTTP 200 with optional commit SHA header and describes invariants FR-F-015-1, NF-004.

Scope (single PR)

- Files to touch: `travelmathlite/core/views.py`, `travelmathlite/urls.py`, `travelmathlite/core/tests/test_health.py`, `docs/ops/logging-and-health.md` (document curl + expected headers).
- Non-goals: providing health metrics beyond successful status or commit SHA.

Standards

- Commits: conventional style (`feat`).
- No secrets; commit SHA read from `LOG_COMMIT_SHA` env (optional). If missing, header omitted.
- Tests rely on `Django TestCase` and `TestCase.client.get('/health/')`.

Acceptance

- `/health/` returns 200 JSON (e.g., `{"status":"ok"}`) and includes `X-Commit-SHA` header when `LOG_COMMIT_SHA` is configured.
- View documented in `docs/ops/logging-and-health.md` with `curl -H "X-Request-ID: ..."` example.
- Document invariants: health endpoint remains accessible even when logging middleware raises.
- Include migration? no.

Prompts for Copilot

- "Create a Django view that returns JSON status 200 and responds with `X-Commit-SHA` header when `LOG_COMMIT_SHA` env var is set."
"Write a simple test that hits `/health/`, asserts 200, JSON payload, and optional header."
