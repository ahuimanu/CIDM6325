# ADR-1.0.5 Forms and HTMX progressive enhancement

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-001, F-003, F-007  
Functional requirements: FR-F-001-2, FR-F-003-1, FR-F-007-1  
Related issues or PRs: #TODO

---

## Intent and scope

Adopt HTMX to enhance forms for calculators while preserving standard POST/GET flows.

In scope: HTMX attributes, partial templates, CSRF, validation UX.  
Out of scope: websockets or long polls.

---

## Problem and forces

- Need responsive feel without a SPA; must degrade gracefully.
- Forces: simple mental model for students; CSRF safety; accessibility.
- Constraints: Vanilla Bootstrap 5; no heavy JS bundlers.

---

## Options considered

- A) HTMX with partials and `hx-post`/`hx-swap`/`hx-target`

  - Pros
    - Minimal JS, progressive enhancement
  - Cons
    - Requires partials discipline
  - Notes
    - Matches PRD intent

- B) Full page reloads only

  - Pros
    - Simplest
  - Cons
    - Worse UX; strays from PRD ACs
  - Notes
    - Acceptable fallback only

---

## Decision

We choose A. Forms render full pages on non-HTMX requests and return partials on HTMX requests, reusing the same views. CSRF included via standard Django template tags.

Decision drivers ranked: UX, simplicity, accessibility.

---

## Consequences

Positive

- Snappy calculator updates; no SPA build
- Shared validation code between full and partial responses

Negative and risks

- Template duplication risk between full and partial

Mitigations

- Use includes/partials pattern and shared blocks

---

## Requirements binding

- FR-F-001-2 Forms validate and normalize inputs (Trace F-001)
- FR-F-003-1 Defaults overrideable via HTMX; errors displayed (Trace F-003)
- NF-002 Accessibility: proper focus and ARIA on updates

---

## Acceptance criteria snapshot

- AC: Calculator submits with HTMX and updates result region without full reload
- AC: Disabling JS still computes results with full reload

Evidence to collect

- Visual check screenshots; functional tests

---

## Implementation outline

Plan

- Add HTMX to base template; add `hx-` attributes to calculator forms
- Detect HTMX via request header; render partials to `templates/calculators/partials/`
- Ensure CSRF tags present; add focus management attributes when needed

Denied paths

- No SPA frameworks or build pipelines

Artifacts to update

- Base template, calculator templates and views, partials

---

## Test plan and invariants

Invariants

- INV-1 Same view covers HTMX and full-page flows
- INV-2 CSRF tokens appear in forms

Unit tests

- RequestFactory tests for both HTMX and non-HTMX requests

Behavioral tests

- Visual script captures HTMX interaction

---

## Documentation updates

- docs/ux/htmx-patterns.md

---

## Rollback and contingency

Rollback trigger

- Complexity creep in templates

Rollback steps

- Remove HTMX attributes and stick to full reloads

Data and config safety

- Pure templates/views; no migrations

---

## Attestation plan

Human witness

- Reviewer confirms both flows work

Attestation record

- Commit hashes and screenshots

---

## Checklist seed

- [ ] HTMX linked in base
- [ ] Partials implemented
- [ ] Non-JS fallback verified

---

## References

- PRD §4 F-001/F-003/F-007; §7 NF-002
