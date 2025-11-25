# ADR-XXXX Title

Date: YYYY-MM-DD  
Status: Proposed | Accepted | Superseded by ADR-YYYY  
Version: 0.1  
Authors: TODO  
Reviewers: TODO  
Supersedes or amends: ADR-____ (optional)

---

## Links and traceability

PRD link: <path-or-section>  
Scope IDs from PRD: F-###, NF-###, OPS-###, DOC-### (list all impacted)  
Functional requirements: FR-F-###-N (list)  
Related issues or PRs: #___, #___

---

## Intent and scope

One short paragraph describing the precise decision and its boundaries.  
In scope: bullets of the affected PRD IDs (F-/NF-/OPS-/DOC-).  
Out of scope: bullets to prevent scope creep.

---

## Problem and forces

- Summary of the problem in 1–2 sentences  
- Key forces and tradeoffs (cost, complexity, pedagogy, security, a11y, performance)  
- Constraints and assumptions (tech choices, environments, team skills)

---

## Options considered

- **A)** Option name  
  - Pros  
  - Cons  
  - Notes on which PRD items it satisfies or strains
- **B)** Option name  
  - Pros  
  - Cons  
  - Notes
- **C)** Option name (optional)  
  - Pros  
  - Cons  
  - Notes

---

## Decision

We choose <A/B/C> because <concise rationale>.  
Decision drivers ranked: D1, D2, D3 (tie back to forces and PRD goals).

---

## Consequences

Positive  
- …

Negative and risks  
- …

Mitigations  
- …

---

## Requirements binding

These are the concrete, testable behaviors this ADR commits to, traceable to the PRD.

- FR-F-###-1 short, testable statement (Trace F-###)  
- FR-F-###-2 short, testable statement (Trace F-###)  
- NF-### measurable target and how it will be verified  
- OPS-### operational outcome and how it will be verified  
- DOC-### documentation deliverable and where it will live

---

## Acceptance criteria snapshot

- AC1 explicit, observable outcome tied to FR-F-###-N  
- AC2 explicit, observable outcome  
- AC3 explicit, observable outcome

Evidence to collect  
- URLs, screenshots, CLI transcripts, validator output, log excerpts

---

## Implementation outline

Plan  
- Step 1 high-level change (files, modules, settings)  
- Step 2 …  
- Step 3 …

Denied paths  
- Approaches we will not take and why (prevents drift)

Artifacts to update  
- Code paths  
- Settings and secrets  
- Migrations  
- Templates and static assets

---

## Test plan and invariants

Invariants  
- INV-1 behavior that must always hold  
- INV-2 …

Unit tests (unittest or Django TestCase)  
- tests/test_…py cases to add or update

Behavioral tests (optional)  
- High-level user flows to cover (if applicable)

Performance and accessibility checks (when applicable)  
- How to measure p95 and with what dataset; how to validate WCAG AA

---

## Documentation updates

- README sections to modify  
- docs/architecture/… narrative or diagram to add  
- docs/security.md notes if relevant  
- CHANGELOG entry

---

## Rollback and contingency

Rollback trigger  
- Observable condition indicating revert (functional, perf, security, a11y)

Rollback steps  
- git revert or feature-flag kill switch  
- Data migration undo plan (if any)

Data and config safety  
- Backups, idempotency, feature flags

---

## Attestation plan

Human witness  
- Who will attest and what proof they will capture

Attestation record  
- Commit hash(es) to cite and brief rationale  
- Path to proof: docs/attestations/ADR-XXXX.md

---

## Checklist seed

- [ ] Traceability fields complete (PRD link, F-/FR-/NF-/OPS-/DOC-)  
- [ ] Decision and drivers documented  
- [ ] Requirements binding lists testable behaviors  
- [ ] Acceptance criteria snapshot defined  
- [ ] Implementation steps and denied paths listed  
- [ ] Tests named with files and invariants specified  
- [ ] Docs updates and changelog listed  
- [ ] Rollback trigger and steps documented  
- [ ] Attestation plan recorded

---

## References

- PRD anchors (section links)  
- Linked issues and PRs  
- External specs or documentation

---

## Usage notes

- Create ADRs as soon as a PRD scope item needs a concrete design or trade-off  
- Fill **Traceability** first so IDs flow through the doc  
- Write **Requirements binding** and **Acceptance criteria** early; they drive tests and the eventual checklist  
- Keep the ADR concise; link to deeper technical docs as needed