# ADR-1.0.11 Testing strategy

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope)  
Scope IDs from PRD: F-011  
Functional requirements: FR-F-011-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define the testing approach using Django TestCase without pytest, including unit tests for calculators/search/auth and mocking external calls.

In scope: test types, fixtures, RequestFactory, time freezing, mocking.  
Out of scope: full CI config specifics.

---

## Problem and forces

- Need confidence without heavy frameworks; ensure deterministic tests.
- Forces: course norms (no pytest), compact yet meaningful coverage.
- Constraints: Limited external dependencies.

---

## Options considered

- A) Django TestCase + standard unittest mocking + freezegun (optional)

  - Pros
    - Aligned with course rules; batteries included
  - Cons
    - Less syntactic sugar
  - Notes
    - Sufficient

- B) pytest-django

  - Pros
    - Rich ecosystem
  - Cons
    - Violates repo norms
  - Notes
    - Not allowed

---

## Decision

We choose A. Emphasize small, deterministic tests per app; RequestFactory for view testing; isolate compute functions.

Decision drivers ranked: alignment with norms, determinism, pedagogy.

---

## Consequences

Positive

- Simple tests students can maintain

Negative and risks

- Less advanced fixtures/plugins

Mitigations

- Provide helper base classes and fixtures where needed

---

## Requirements binding

- FR-F-011-1 Cover calculators, search, and auth flows (Trace F-011)
- NF-004 Reliability: tests validate idempotent import and health endpoint

---

## Acceptance criteria snapshot

- AC: Tests exist per app covering happy paths and 1–2 edge cases
- AC: External network calls are mocked; times frozen where needed

Evidence to collect

- Test run transcript

---

## Implementation outline

Plan

- Add tests in `apps/*/tests.py`; use factories/fixtures as needed
- Add unit tests for `calculators/geo.py` and `costs.py`
- Mock import downloads and health endpoints where applicable

Denied paths

- No pytest

Artifacts to update

- Tests across apps; docs/testing.md

---

## Test plan and invariants

Invariants

- INV-1 Tests deterministic and isolated; no real network calls

Unit tests

- Listed above

Behavioral tests

- Visual script runs alongside tests for optional checks

---

## Documentation updates

- docs/testing.md

---

## Rollback and contingency

Rollback trigger

- Tests flaky or too slow

Rollback steps

- Reduce scope or tighten mocking

Data and config safety

- Tests only; no data impact

---

## Attestation plan

Human witness

- Reviewer checks coverage of critical paths

Attestation record

- Commit hash and CI transcript

---

## Checklist seed

- [ ] TestCase used across apps
- [ ] Key flows covered
- [ ] External calls mocked

---

## References

- PRD §4 F-011
