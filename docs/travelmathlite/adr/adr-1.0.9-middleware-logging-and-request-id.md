# ADR-1.0.9 Middleware, logging, and request ID

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#11-success-metrics (Success metrics)  
Scope IDs from PRD: F-009, F-015  
Functional requirements: FR-F-009-1, FR-F-015-1  
Related issues or PRs: #TODO

---

## Intent and scope

Add a custom middleware to inject an `X-Request-ID` and measure request duration; configure structured logging and a health endpoint.

In scope: middleware, logging format, health view.  
Out of scope: full observability stack (handled separately).

---

## Problem and forces

- Need traceability across logs and basic health signal.
- Forces: low overhead, easy to reason about, consistent format.
- Constraints: No external log collectors required.

---

## Options considered

- A) Custom lightweight middleware + Python logging JSON formatter

  - Pros
    - Minimal; tailored to needs
  - Cons
    - Build formatting ourselves
  - Notes
    - Good for teaching

- B) Third-party request ID package and logging framework

  - Pros
    - Feature-rich
  - Cons
    - Extra deps; black box
  - Notes
    - Unnecessary

---

## Decision

We choose A. Middleware sets/request ID and duration; logging configured to include level, module, request_id, and duration_ms. Health endpoint returns 200 and optionally commit SHA from env.

Decision drivers ranked: simplicity, visibility, minimal deps.

---

## Consequences

Positive

- Easy correlation of logs per request; simple uptime check

Negative and risks

- DIY JSON formatting may be basic

Mitigations

- Keep format small and documented; swap formatter later if needed

---

## Requirements binding

- FR-F-009-1 Add request ID and duration to logs (Trace F-009)
- FR-F-015-1 Structured logging and error pages (Trace F-015)
- NF-004 Reliability: health endpoint 200

---

## Acceptance criteria snapshot

- AC: Logs contain request_id and duration_ms fields
- AC: `/health/` returns OK with commit SHA header when set

Evidence to collect

- Log snippet; curl output

---

## Implementation outline

Plan

- Create `core/middleware.py` with request ID and timing
- Configure logging dictConfig formatter emitting JSON lines
- Add `/health/` view returning OK and commit SHA

Denied paths

- No heavy logging frameworks

Artifacts to update

- Middleware module, settings LOGGING, project urls

---

## Test plan and invariants

Invariants

- INV-1 Request ID present for every request
- INV-2 Duration measured and logged

Unit tests

- Middleware tests using RequestFactory; health view test

Behavioral tests

- Manual curl and log inspection

---

## Documentation updates

- docs/ops/logging-and-health.md

---

## Rollback and contingency

Rollback trigger

- Log volume or format issues

Rollback steps

- Switch to simpler text formatter temporarily

Data and config safety

- Config-only; no data impact

---

## Attestation plan

Human witness

- Reviewer checks logs and health endpoint

Attestation record

- Commit and transcript

---

## Checklist seed

- [ ] Middleware created and enabled
- [ ] JSON logging configured
- [ ] Health endpoint added

---

## References

- PRD §4 F-009/F-015; §11 Success metrics
