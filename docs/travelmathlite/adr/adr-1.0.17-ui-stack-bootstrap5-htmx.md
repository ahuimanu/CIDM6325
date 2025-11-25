# ADR-1.0.17 UI stack: Bootstrap 5 + HTMX, no SPA

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope)  
Scope IDs from PRD: F-007, F-001, F-003, F-008  
Functional requirements: FR-F-007-1, FR-F-001-2, FR-F-003-1, FR-F-008-1  
Related issues or PRs: #TODO

---

## Intent and scope

Standardize on vanilla Bootstrap 5 for layout and components with HTMX for progressive enhancement; avoid SPA frameworks and bundlers.

In scope: CSS/JS includes, component patterns, navbar/footer, partials.  
Out of scope: React/Vue/Angular or build pipelines.

---

## Problem and forces

- Need responsive UI that is easy to reason about and customize.
- Forces: minimal dependencies; consistent look; accessible defaults.
- Constraints: No bundlers; use CDN or vendored assets.

---

## Options considered

- A) Bootstrap 5 + HTMX + a few utility classes

  - Pros
    - Fast to build; accessible; no build step
  - Cons
    - Less custom than a bespoke design
  - Notes
    - Meets PRD needs

- B) TailwindCSS or custom SCSS build

  - Pros
    - Highly customizable
  - Cons
    - Requires build tooling; steeper learning
  - Notes
    - Out of scope

---

## Decision

We choose A. Use CDN Bootstrap in local; pin versions in prod. HTMX added globally; components (forms, navbar, pagination, alerts) follow Bootstrap patterns.

Decision drivers ranked: speed, accessibility, simplicity.

---

## Consequences

Positive

- Rapid development; consistent components

Negative and risks

- Limited customization without a build step

Mitigations

- Small CSS overrides file; document patterns

---

## Requirements binding

- FR-F-007-1 Base template with Bootstrap 5, navbar, footer (Trace F-007)
- FR-F-001-2/FR-F-003-1 Forms styled and usable (Trace F-001/F-003)
- FR-F-008-1 Pagination and highlights use Bootstrap classes (Trace F-008)

---

## Acceptance criteria snapshot

- AC: Base template loads Bootstrap and HTMX; navbar works on mobile
- AC: Forms and pagination follow Bootstrap styling and are accessible

Evidence to collect

- Screenshots; generated HTML snippets

---

## Implementation outline

Plan

- Add base template with CDN Bootstrap and HTMX; defer scripts appropriately
- Create includes for navbar/footer/alerts; ensure sticky footer
- Style partials consistently

Denied paths

- No SPA or heavy JS toolchains

Artifacts to update

- `templates/base.html`, `templates/includes/*`, static overrides

---

## Test plan and invariants

Invariants

- INV-1 Assets load; responsive navbar collapses correctly

Unit tests

- Template asserts for includes; optional visual tests

Behavioral tests

- Visual check script screenshots

---

## Documentation updates

- docs/ux/ui-stack.md

---

## Rollback and contingency

Rollback trigger

- Asset load failures or accessibility regressions

Rollback steps

- Swap to local vendored assets; revert overrides

Data and config safety

- UI-only

---

## Attestation plan

Human witness

- Reviewer checks screenshots and markup

Attestation record

- Commit and images

---

## Checklist seed

- [ ] Base template added
- [ ] Includes created
- [ ] Overrides documented

---

## References

- PRD §4 F-007 and related items
