# ADR-1.0.6 Authentication and saved calculations model

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope)  
Scope IDs from PRD: F-006  
Functional requirements: FR-F-006-1  
Related issues or PRs: #TODO

---

## Intent and scope

Use Django auth views for login/logout/register and introduce a `SavedCalculation` model to store a user's last 10 calculator runs. Migrate anonymous session-stored inputs to user upon login.

In scope: models, limits, session migration, privacy.  
Out of scope: social auth, email verification flows.

---

## Problem and forces

- Users want persistence across sessions; anonymous users still need convenience.
- Forces: leverage Django batteries; keep data small and private.
- Constraints: No heavy profile features; course time.

---

## Options considered

- A) Custom auth flows and models

  - Pros
    - Full control
  - Cons
    - Unnecessary complexity
  - Notes
    - Not aligned with PRD simplicity

- B) Django built-in auth views + lightweight `SavedCalculation` model

  - Pros
    - Fast to implement; secure by default
  - Cons
    - Limited customization
  - Notes
    - Good fit

---

## Decision

We choose B. Use built-in auth templates (overridable) and a `SavedCalculation` with fields: user(FK), calculator_type, inputs(JSON), outputs(JSON), created_at. Cap at 10 per user via manager housekeeping.

Decision drivers ranked: speed, security, simplicity.

---

## Consequences

Positive

- Minimal code for auth; simple persistence structure
- Clear place to hang future features like sharing/export

Negative and risks

- JSON fields portability on SQLite vs Postgres

Mitigations

- Store as TextField JSON serialized; keep schema small; optionally use JSONField on Postgres

---

## Requirements binding

- FR-F-006-1 Save last 10 calculations with list/delete (Trace F-006)
- NF-003 Security: per-user access control; private by default

---

## Acceptance criteria snapshot

- AC: Auth views work with our templates
- AC: After login, last anonymous inputs migrate and first save occurs on next calc
- AC: Saved list limited to 10; older entries pruned

Evidence to collect

- Tests for session migration; screenshots of saved list

---

## Implementation outline

Plan

- Add `apps/trips/models.py` with `SavedCalculation`; admin registration
- Middleware or post-login hook to migrate session inputs
- Views and templates to list/delete entries

Denied paths

- No social login in MVP

Artifacts to update

- Accounts templates, trips views/templates, tests

---

## Test plan and invariants

Invariants

- INV-1 Users see only their own saved items
- INV-2 At most 10 items retained per user

Unit tests

- Tests for creation, pruning, list, delete, and session migration

Behavioral tests

- Manual flow from anonymous calc → login → saved list

---

## Documentation updates

- docs/features/saved-calculations.md

---

## Rollback and contingency

Rollback trigger

- Complexity or reliability issues with session migration

Rollback steps

- Disable migration; keep anonymous-only persistence

Data and config safety

- Simple model with no critical data; safe to revert

---

## Attestation plan

Human witness

- Reviewer validates list/delete and cap behavior

Attestation record

- Commit hashes and test evidence

---

## Checklist seed

- [ ] Auth views wired and themed
- [ ] Model, pruning, and migration implemented
- [ ] Tests pass for list/delete/cap

---

## References

- PRD §4 F-006; §7 NF-003
