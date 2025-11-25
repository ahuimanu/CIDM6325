# BRIEF: Document logging and health invariants

Goal

- Ship `docs/ops/logging-and-health.md` describing middleware/log structure, health curl sample, tests to run, covering NF-004 reliability.

Scope (single PR)

- Files to touch: `docs/ops/logging-and-health.md`, `travelmathlite/core/tests/__init__.py` (test helpers), README updates if needed, `travelmathlite/scripts/visual_check` if relevant.
- Non-goals: tutorial-level guides beyond the minimal ops doc.

Standards

- Commits: conventional style (`docs`).
- No secrets; doc should mention reading `LOG_COMMIT_SHA` via env.
- Tests referenced should be runnable via `uv run python travelmathlite/manage.py test travelmathlite.core.tests`.

Acceptance

- Operations doc includes middleware/logging overview, sample `curl http://localhost:8000/health/` output, and instructions for verifying logs contain `request_id`/`duration_ms` using `tail`/`jq`.
- Doc mentions invariants: INV-1 request ID per request, INV-2 health endpoint 200, INV-3 logs include duration.
- Testing section lists commands, e.g., `uv run python manage.py test travelmathlite.core.tests.test_middleware` and `travelmathlite.core.tests.test_health`.
- Include migration? no.

Prompts for Copilot

- "Write a Markdown ops guide summarizing the new middleware, logging JSON fields, and health endpoint plus a sample curl command and log snippet."
- "List the tests to run and the invariants they cover."
