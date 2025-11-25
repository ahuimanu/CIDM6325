# ADR-1.0.15 Accessibility standards

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional - Accessibility)  
Scope IDs from PRD: F-007, F-008  
Functional requirements: FR-F-007-1, FR-F-008-1  
Related issues or PRs: #TODO

---

## Intent and scope

Adopt WCAG AA targets for color contrast, keyboard navigability, and proper ARIA where needed, with manual and tool-assisted checks.

In scope: contrast, focus states, form labeling, keyboard navigation.  
Out of scope: full ADA audit.

---

## Problem and forces

- Need inclusive UI; Bootstrap defaults help but must be verified.
- Forces: practical checks within course time.
- Constraints: No dedicated accessibility team.

---

## Options considered

- A) Use Bootstrap 5 defaults + axe DevTools/manual checks; fix issues found

  - Pros
    - Fast; pragmatic
  - Cons
    - Limited depth
  - Notes
    - Adequate for PRD

- B) Deep a11y automation and audits

  - Pros
    - Thorough
  - Cons
    - Out of scope
  - Notes
    - Future option

---

## Decision

We choose A. Ensure focus styles are visible, form fields have labels, and color contrast passes; HTMX updates manage focus sensibly.

Decision drivers ranked: inclusivity, practicality, clarity.

---

## Consequences

Positive

- Better usability for keyboard and screen-reader users

Negative and risks

- Some nuanced issues may remain unaddressed

Mitigations

- Document open issues and fixes as we iterate

---

## Requirements binding

- FR-F-007-1 Accessibility: color contrast, focus, ARIA (Trace F-007)
- FR-F-008-1 Search templates respect accessibility patterns (Trace F-008)
- NF-002 Accessibility checks via axe and manual review

---

## Acceptance criteria snapshot

- AC: axe DevTools reports no critical violations on key pages
- AC: Keyboard-only navigation reaches and operates forms and results

Evidence to collect

- axe report screenshots; notes on manual checks

---

## Implementation outline

Plan

- Verify color tokens and contrast; adjust CSS if needed
- Ensure `aria-live` or focus management on HTMX result regions
- Add `for`/`id` pairs and `aria-describedby` where relevant

Denied paths

- No heavy automation suites

Artifacts to update

- Base and feature templates; small CSS overrides

---

## Test plan and invariants

Invariants

- INV-1 Forms are operable via keyboard alone

Unit tests

- N/A (manual/tool-based checks primarily)

Behavioral tests

- Manual and axe checks recorded

---

## Documentation updates

- docs/ux/accessibility.md

---

## Rollback and contingency

Rollback trigger

- Regressions found in checks

Rollback steps

- Revert problematic CSS or templates and re-test

Data and config safety

- UI-only changes

---

## Attestation plan

Human witness

- Reviewer attaches axe report

Attestation record

- Commit hash and screenshots

---

## Checklist seed

- [ ] Contrast validated
- [ ] Keyboard navigation verified
- [ ] HTMX focus management reviewed

---

## References

- PRD §7 NF-002; §4 F-007/F-008
