# ADR-1.0.10 Caching strategy

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#7-non-functional-requirements (Non functional)  
Scope IDs from PRD: F-013  
Functional requirements: FR-F-013-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define caching approach for search and airport endpoints and specify cache backend choices for local/prod.

In scope: per-view caching, low-level caching, cache headers, backend choices.  
Out of scope: CDN layer.

---

## Problem and forces

- Improve response times for repeated queries; keep code simple.
- Forces: dev-first, no external infra by default; optional production backend.
- Constraints: Avoid complexity; keep cache keys deterministic.

---

## Options considered

- A) Django locmem cache in dev; file-based or Redis in prod (optional)

  - Pros
    - Zero-setup locally; scalable option later
  - Cons
    - Locmem not shared across processes
  - Notes
    - Acceptable for demo

- B) No caching

  - Pros
    - Simplest
  - Cons
    - Misses PRD perf goals
  - Notes
    - Not acceptable

---

## Decision

We choose A. Per-view caching for search results and nearest-airport views with short TTLs (e.g., 5–15 minutes). Optionally enable Redis in prod via `CACHES` URL.

Decision drivers ranked: simplicity, performance, portability.

---

## Consequences

Positive

- Faster repeated requests; easy to configure

Negative and risks

- Stale results possible if datasets change

Mitigations

- Short TTLs; manual invalidation helper for dataset imports

---

## Requirements binding

- FR-F-013-1 Enable per-view/low-level caching on hot paths (Trace F-013)
- NF-001 Performance: p95 targets met locally

---

## Acceptance criteria snapshot

- AC: Cache hit rate visible via logging; repeated search queries are faster

Evidence to collect

- Timing logs before/after enabling cache; settings snippet

---

## Implementation outline

Plan

- Configure `CACHES` for locmem by default; allow env-based override
- Decorate hot views with `@cache_page` and/or use low-level cache for computed lists
- Add cache headers where appropriate

Denied paths

- No complex invalidation logic in MVP

Artifacts to update

- Settings, views, helpers

---

## Test plan and invariants

Invariants

- INV-1 Cache TTLs respected; content varies by query params

Unit tests

- Tests that repeat calls within TTL are faster or show cache marker

Behavioral tests

- Manual run with timing logs

---

## Documentation updates

- docs/perf/caching.md

---

## Rollback and contingency

Rollback trigger

- Cache causing stale or incorrect outputs

Rollback steps

- Disable decorators and flush cache

Data and config safety

- Config-only and ephemeral data

---

## Attestation plan

Human witness

- Reviewer checks logs and verifies speed-up

Attestation record

- Commit hash and timing evidence

---

## Checklist seed

- [ ] Cache backend configured
- [ ] Cache decorators applied
- [ ] Short TTLs documented

---

## References

- PRD §4 F-013; §7 NF-001
