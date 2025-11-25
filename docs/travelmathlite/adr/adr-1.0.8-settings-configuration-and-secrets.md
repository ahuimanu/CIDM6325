# ADR-1.0.8 Settings configuration and secrets

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-012  
Functional requirements: FR-F-012-1  
Related issues or PRs: #TODO

---

## Intent and scope

Split settings into base/local/prod and read configuration from environment using `django-environ`.

In scope: settings split, env variables, defaults.  
Out of scope: containerization or infra provisioning.

---

## Problem and forces

- Need safe defaults and easy local overrides; keep secrets out of code.
- Forces: 12-factor alignment; simplicity for students.
- Constraints: Single repo, possibly no container runtime in class.

---

## Options considered

- A) Single settings.py with inline env reads

  - Pros
    - Minimal files
  - Cons
    - Hard to reason about prod vs local
  - Notes
    - Not ideal for teaching

- B) Split base/local/prod using `django-environ`

  - Pros
    - Clear separation; secure defaults
  - Cons
    - Slightly more boilerplate
  - Notes
    - Matches PRD

---

## Decision

We choose B. `settings/base.py` contains common config; `local.py` enables debug and dev tools; `prod.py` enforces `DEBUG=False`, `ALLOWED_HOSTS`, security headers, and WhiteNoise.

Decision drivers ranked: safety, clarity, pedagogy.

---

## Consequences

Positive

- Safer production defaults; easier to teach differences

Negative and risks

- Slight overhead managing multiple files

Mitigations

- Provide `.env.example` and docs for required variables

---

## Requirements binding

- FR-F-012-1 Split settings and secure prod defaults (Trace F-012)
- NF-003 Security: secure cookies, CSRF, headers configured in prod

---

## Acceptance criteria snapshot

- AC: Running with `DJANGO_SETTINGS_MODULE=...prod` disables debug and requires hosts
- AC: `.env` drives local config; secrets not committed

Evidence to collect

- Settings diff, run transcript, `.env.example` file

---

## Implementation outline

Plan

- Create `project/settings/{base,local,prod}.py`
- Add `django-environ`; parse envs (secret key, DB URL, email, etc.)
- Configure security headers in prod

Denied paths

- No secrets in repo

Artifacts to update

- Settings, README, docs/ops/settings.md

---

## Test plan and invariants

Invariants

- INV-1 `DEBUG=False` in prod; `ALLOWED_HOSTS` enforced
- INV-2 Security middleware enabled in prod

Unit tests

- Settings assertions using override settings or simple import tests

Behavioral tests

- Manual run of local and prod settings

---

## Documentation updates

- `.env.example` and docs/ops/settings.md

---

## Rollback and contingency

Rollback trigger

- Misconfiguration or friction for students

Rollback steps

- Consolidate to single settings temporarily while debugging

Data and config safety

- Config-only changes; no migrations

---

## Attestation plan

Human witness

- Reviewer verifies prod settings effect and `.env` usage

Attestation record

- Commit hash and transcript

---

## Checklist seed

- [ ] Split settings created
- [ ] `.env.example` added
- [ ] Security headers configured in prod

---

## References

- PRD §4 F-012; §7 NF-003
