# ADR-1.0.13 Observability and error handling

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#11-success-metrics (Success metrics)  
Scope IDs from PRD: F-015, F-009  
Functional requirements: FR-F-015-1, FR-F-009-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define structured logging format, error page customization, and optional Sentry integration guidance.

In scope: logging fields, error templates, Sentry toggle.  
Out of scope: full APM.

---

## Problem and forces

- Need actionable logs and user-friendly error pages.
- Forces: low-dep approach, optional third-party.
- Constraints: Classroom environment.

---

## Options considered

- A) Python logging JSON lines with request_id, duration, path, status; custom 404/500 templates; optional Sentry DSN via env

  - Pros
    - Minimal; flexible
  - Cons
    - DIY formatting
  - Notes
    - Fine for course

- B) Full logging stack

  - Pros
    - Powerful
  - Cons
    - Overkill
  - Notes
    - Not needed

---

## Decision

We choose A. Emit JSON lines; add `404.html` and `500.html`; document optional Sentry DSN usage without enabling by default.

Decision drivers ranked: usefulness, simplicity, opt-in.

---

## Consequences

Positive

- Logs that support debugging without extra infra

Negative and risks

- Limited analytics without APM

Mitigations

- Provide how-to for enabling Sentry later

---

## Requirements binding

- FR-F-015-1 Structured logs and error pages (Trace F-015)
- FR-F-009-1 Request ID is included (Trace F-009)

---

## Acceptance criteria snapshot

- AC: 404/500 templates render; logs include request_id and status

Evidence to collect

- Screenshots and log snippets

---

## Implementation outline

Plan

- Configure logging; implement error templates in `templates/`
- Add Sentry init block guarded by env

Denied paths

- No mandatory third-party SDKs

Artifacts to update

- Settings LOGGING, templates/404.html and 500.html

---

## Test plan and invariants

Invariants

- INV-1 Errors include request_id in logs

Unit tests

- Trigger 404 via test client; assert template and log call

Behavioral tests

- Manual check of 500 page in DEBUG=False

---

## Documentation updates

- docs/ops/logging-and-errors.md

---

## Rollback and contingency

Rollback trigger

- Log parsing issues or noisy output

Rollback steps

- Switch to simpler console formatter

Data and config safety

- Config-only

---

## Attestation plan

Human witness

- Reviewer verifies error pages and log fields

Attestation record

- Commit hash and sample logs

---

## Checklist seed

- [ ] JSON logging configured
- [ ] 404/500 templates created
- [ ] Optional Sentry documented

---

## References

- PRD §4 F-015; §11 Success metrics
