# ADR-1.0.14 Deployment approach

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#12-rollout-and-release-plan (Rollout)  
Scope IDs from PRD: F-012, F-010, F-015  
Functional requirements: FR-F-012-1, FR-F-010-1, FR-F-015-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define a simple deployment target suitable for demos: gunicorn + WhiteNoise for static, environment-driven config, HTTPS-ready.

In scope: app server choice, static serving, settings selection.  
Out of scope: full container orchestration.

---

## Problem and forces

- Need a realistic yet simple deployment story for demos.
- Forces: minimal infra, clear steps, portability.
- Constraints: No managed cloud required for course.

---

## Options considered

- A) Gunicorn + WhiteNoise on a small VM or PaaS; env vars; `prod` settings

  - Pros
    - Minimal moving parts; aligns to static strategy ADR
  - Cons
    - Not horizontally scalable by default
  - Notes
    - Fine for demos

- B) Django dev server

  - Pros
    - Easiest
  - Cons
    - Not suitable beyond local dev
  - Notes
    - Not acceptable for demo

---

## Decision

We choose A. Document run command, environment variables, and collectstatic step. Recommend reverse proxy/HTTPS when available; otherwise PaaS SSL.

Decision drivers ranked: simplicity, correctness, documentation clarity.

---

## Consequences

Positive

- Straightforward instructions; mirrors production patterns

Negative and risks

- Limited performance if traffic spikes

Mitigations

- Document scaling tips; suggest moving to NGINX/CDN later

---

## Requirements binding

- FR-F-012-1 Prod settings applied with security headers (Trace F-012)
- FR-F-010-1 collectstatic and hashed filenames (Trace F-010)
- FR-F-015-1 structured logs usable in demo env (Trace F-015)

---

## Acceptance criteria snapshot

- AC: Deploy guide yields a running app with hashed static and health endpoint OK

Evidence to collect

- Transcript and screenshot of deployed app

---

## Implementation outline

Plan

- Provide Procfile or run docs for gunicorn
- Ensure `DJANGO_SETTINGS_MODULE=...prod` and envs documented
- Add deploy checklist in docs

Denied paths

- No container orchestration in MVP

Artifacts to update

- docs/ops/deploy.md, README quickstart

---

## Test plan and invariants

Invariants

- INV-1 App starts with prod settings locally

Unit tests

- N/A

Behavioral tests

- Manual deploy smoke test

---

## Documentation updates

- docs/ops/deploy.md

---

## Rollback and contingency

Rollback trigger

- Deploy fails or app crashes in prod settings

Rollback steps

- Revert to local settings; iterate fix; redeploy

Data and config safety

- Config-only; backups for DB if used remotely

---

## Attestation plan

Human witness

- Reviewer validates deploy steps

Attestation record

- Commit and screenshot

---

## Checklist seed

- [ ] Gunicorn command documented
- [ ] Prod env vars listed
- [ ] collectstatic step included

---

## References

- PRD §12 Rollout and release plan
