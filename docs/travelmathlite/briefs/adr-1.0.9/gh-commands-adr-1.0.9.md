# GitHub CLI Commands for ADR-1.0.9 Middleware + Logging

This document captures reusable `gh` commands for creating issues that align with the ADR-1.0.9 briefs.

---

## Prerequisites

```bash
# Check labels before issuing new ones
gh label list

# Sync with branch
git checkout FALL2025
git pull origin FALL2025
```

---

## Brief 01 — Request-ID middleware

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.9-01: Middleware with request ID and timing" \
  -b "**Goal:** Add middleware that injects `X-Request-ID` and records duration for each request.

**Scope:** PRD §4 F-009, FR-F-009-1, NF-004
**Files:** `travelmathlite/core/middleware.py`, `travelmathlite/settings.py`, `travelmathlite/core/tests/test_middleware.py`
**Acceptance:** request ID present on response, duration accessible, invariants INV-1/INV-2
**Brief:** docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-01-request-id-middleware.md" \
  -l feature,FR,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

## Brief 02 — Structured JSON logging

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.9-02: Structured JSON logging" \
  -b "**Goal:** Configure dictConfig to emit JSON lines with level, module, request_id, and duration_ms.

**Scope:** PRD §4 F-015, FR-F-015-1
**Files:** `travelmathlite/settings.py`, `travelmathlite/core/tests/test_logging.py`, `docs/ops/logging-and-health.md`
**Acceptance:** JSON logs include request metadata, documented invariants document INV-1/INV-2
**Brief:** docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-02-structured-logging.md" \
  -l feature,FR,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

## Brief 03 — Health endpoint

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.9-03: Health endpoint" \
  -b "**Goal:** Add `/health/` that returns 200 with optional `X-Commit-SHA` header and docs.

**Scope:** NF-004 reliability
**Files:** `travelmathlite/core/views.py`, `travelmathlite/urls.py`, `travelmathlite/core/tests/test_health.py`
**Acceptance:** curl shows status OK, header present when env set, invariants include health accessibility
**Brief:** docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-03-health-endpoint.md" \
  -l feature,NF,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

## Brief 04 — Docs + tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.9-04: Logging & health docs" \
  -b "**Goal:** Document the middleware/logging behavior plus tests and verification commands.

**Scope:** Documentation updates supporting NF-004
**Files:** `docs/ops/logging-and-health.md`
**Acceptance:** Ops guide includes curl/log samples and commands, test suite references INV-1/INV-2/INV-3
**Brief:** docs/travelmathlite/briefs/adr-1.0.9/brief-ADR-1.0.9-04-docs-and-tests.md" \
  -l docs,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

---

## Workflow reminder (optional)

```bash
# Use Refs/Closes keywords and mirror commit messages as issue comments.
# Example ongoing commit: `feat: add request id middleware — Refs #${ISSUE_01}`
# Finalizing commit: `feat: finalize middleware + logging — Closes #${ISSUE_01}`
```
