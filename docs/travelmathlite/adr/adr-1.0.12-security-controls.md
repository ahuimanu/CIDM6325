# ADR-1.0.12 Security controls

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-014, F-006, F-012  
Functional requirements: FR-F-014-1, FR-F-012-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define security posture: CSRF, input sanitization, auth hardening, optional rate limiting and CAPTCHA.

In scope: settings, validators, sanitization library where needed, rate limiting choice.  
Out of scope: full enterprise IAM.

---

## Problem and forces

- Need safe defaults and protections for auth endpoints and user input.
- Forces: minimal deps, clarity for students, measurable controls.
- Constraints: Keep optional features (rate limit/CAPTCHA) easy to toggle.

---

## Options considered

- A) Django built-ins (CSRF, SecurityMiddleware, validators) + `bleach` for any rich text + `django-ratelimit` for auth endpoints

  - Pros
    - Strong defaults; easy to wire; measurable
  - Cons
    - Extra deps (small)
  - Notes
    - Good balance

- B) Only built-ins, no rate limiting or sanitization

  - Pros
    - Fewer deps
  - Cons
    - Weaker protections against abuse/XSS
  - Notes
    - Not preferred

---

## Decision

We choose A. Enable built-ins; add `django-ratelimit` on login/register and `bleach` where any user-provided HTML might render (if added), otherwise rely on autoescape.

Decision drivers ranked: security, simplicity, measurability.

---

## Consequences

Positive

- Hardened auth paths; safer rendering

Negative and risks

- Slight complexity configuring rate limits

Mitigations

- Centralize settings; document toggles; provide sensible defaults

---

## Requirements binding

- FR-F-014-1 Harden auth and rate-limit sensitive endpoints (Trace F-014)
- FR-F-012-1 Security headers and secure cookies in prod (Trace F-012)
- NF-003 Security checks documented and tested

---

## Acceptance criteria snapshot

- AC: CSRF enabled on forms; secure headers verified in prod
- AC: Rate limiting returns 429 on abusive endpoint patterns (when enabled)

Evidence to collect

- Settings inspection; test outputs for rate limit

---

## Implementation outline

Plan

- Ensure SecurityMiddleware, CSRF, and validators configured
- Add `django-ratelimit` to auth views with reasonable limits
- Use `bleach` only if rendering any HTML from users; otherwise rely on autoescape

Denied paths

- No custom crypto or homegrown auth

Artifacts to update

- Settings, auth view decorators, docs/security.md

---

## Test plan and invariants

Invariants

- INV-1 CSRF tokens present and validated
- INV-2 Rate-limited views enforce configured thresholds

Unit tests

- Tests for rate-limited views; header checks in prod settings

Behavioral tests

- Manual attempt at repeated login

---

## Documentation updates

- docs/security.md with toggles and defaults

---

## Rollback and contingency

Rollback trigger

- False positives on rate limiting; user lockouts

Rollback steps

- Disable rate limiters quickly via settings flags

Data and config safety

- Config-only; no data risk

---

## Attestation plan

Human witness

- Reviewer verifies headers and rate limit behavior

Attestation record

- Commit hashes and test transcript

---

## Checklist seed

- [ ] Security middleware and headers verified
- [ ] Rate limiting applied to auth endpoints
- [ ] Autoescape and/or bleach coverage documented

---

## References

- PRD §4 F-014/F-012; §7 NF-003
