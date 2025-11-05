# ADR-1.0.7 Static, media, and asset pipeline

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-007, F-010  
Functional requirements: FR-F-007-1, FR-F-010-1  
Related issues or PRs: #TODO

---

## Intent and scope

Choose how to manage static files, hashing, and optional media (avatars) across local and production settings.

In scope: storage backend, collectstatic, WhiteNoise, folder layout.  
Out of scope: CDN integration.

---

## Problem and forces

- Need reliable static handling for Bootstrap assets and branding; hashed filenames in prod.
- Forces: simple deployment, minimal infra, consistent across environments.
- Constraints: Course-friendly; no external CDN required.

---

## Options considered

- A) Django StaticFiles + ManifestStaticFilesStorage + WhiteNoise in prod

  - Pros
    - Simple; hashes for cache-busting; one-process serving OK for demo
  - Cons
    - Not optimal for large scale
  - Notes
    - Best for this project

- B) Reverse proxy/NGINX for static

  - Pros
    - Production-grade
  - Cons
    - Extra infra/config beyond course scope
  - Notes
    - Future option

---

## Decision

We choose A. Use ManifestStaticFilesStorage in prod and WhiteNoise for serving. Media configured with `MEDIA_ROOT`/`MEDIA_URL`; optional avatar upload guarded to local/demo.

Decision drivers ranked: simplicity, correctness, low-ops.

---

## Consequences

Positive

- Predictable static pipeline; cache-busting via hashed filenames

Negative and risks

- WhiteNoise throughput is limited vs CDN/nginx

Mitigations

- Keep assets small; document future CDN path

---

## Requirements binding

- FR-F-010-1 Configure static/media with hashed filenames (Trace F-010)
- FR-F-007-1 Base template includes assets; navbar/footer implemented (Trace F-007)
- NF-004 Reliability: collectstatic required in prod builds

---

## Acceptance criteria snapshot

- AC: `collectstatic` produces hashed files; app serves them via WhiteNoise in prod
- AC: Avatar upload works in local; media served correctly

Evidence to collect

- Terminal transcript; screenshot of network panel showing hashed asset

---

## Implementation outline

Plan

- Configure `STATICFILES_DIRS`, `STATIC_ROOT`, `MEDIA_ROOT`/`MEDIA_URL`
- Enable `ManifestStaticFilesStorage` in prod settings
- Add WhiteNoise middleware/setting in prod

Denied paths

- No CDN wiring in MVP

Artifacts to update

- Settings files, base template, static/ and media/ folders

---

## Test plan and invariants

Invariants

- INV-1 Static URLs resolve in templates
- INV-2 Manifest storage rewrites links correctly

Unit tests

- Template rendering asserts expected static URLs

Behavioral tests

- Visual check script loads Bootstrap CSS/JS; avatar upload tested locally

---

## Documentation updates

- docs/ops/static-and-media.md

---

## Rollback and contingency

Rollback trigger

- Static files not loading in prod

Rollback steps

- Switch WhiteNoise off and serve via dev server temporarily while fixing

Data and config safety

- No data impact; config-only

---

## Attestation plan

Human witness

- Reviewer validates hashed assets and serving behavior

Attestation record

- Commit hash and screenshots

---

## Checklist seed

- [ ] Manifest storage enabled in prod
- [ ] WhiteNoise configured
- [ ] Avatar/media path verified

---

## References

- PRD §4 F-007/F-010; §7 NF-004
