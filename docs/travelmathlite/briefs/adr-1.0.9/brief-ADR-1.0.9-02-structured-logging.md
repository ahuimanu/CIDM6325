# BRIEF: Build structured JSON logging

Goal

- Configure Django logging to emit JSON lines with `request_id`, `duration_ms`, `level`, and `module`, satisfying FR-F-015-1 and NF-004 logging expectations.

Scope (single PR)

- Files to touch: `travelmathlite/settings.py`, any helper module for logging formatter (e.g., `travelmathlite/core/logging.py`), `docs/ops/logging-and-health.md` (document format/sample), `travelmathlite/core/tests/test_logging.py`.
- Non-goals: migrating to third-party logging frameworks or logging more than specified fields.

Standards

- Commits: conventional style (`feat`).
- No secrets; serializer reads env `LOG_COMMIT_SHA` for health docs only.
- Tests use Django `TestCase` or `SimpleTestCase` to assert handler output.

Acceptance

- Logging dictConfig emits JSON lines on `stdout` with fields `timestamp`, `level`, `module`, `message`, `request_id`, `duration_ms`.
- Duration reflects middleware value; missing request_id should fall back to `-` or uuid.
- Include logging sample in docs and CLI command verifying log format (e.g., `uv run python manage.py check --verbosity=2`).
- Include migration? no.
- Document invariants in docs (INV-1/INV-2 referencing request IDs/duration).

Prompts for Copilot

- "Generate a Django `LOGGING` dictConfig that uses `logging.StreamHandler` and a custom formatter outputting JSON with request metadata, level, module, and time."
"Add a helper that formats records, pulling `request_id`/`duration_ms` from the record or thread local storage if missing."
