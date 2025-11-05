# ADR-1.0.4 Search strategy and URL design

Date: 2025-11-02  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#10-acceptance-criteria (Acceptance)  
Scope IDs from PRD: F-008, F-007  
Functional requirements: FR-F-008-1, FR-F-007-1  
Related issues or PRs: #TODO

---

## Intent and scope

Define search behavior for cities and airports and friendly URL conventions with namespacing and canonical links.

In scope: query parsing, DB filtering, pagination, highlighting, URL shapes, canonical/robots.  
Out of scope: airport nearest lookup (ADR-1.0.3).

---

## Problem and forces

- Need discoverable, shareable URLs and simple search with pagination and highlights.
- Forces: SQLite-first (no trigram), good UX, consistent templates, SEO basics (sitemap/robots/canonical).
- Constraints: Keep it simple and fast for class environments.

---

## Options considered

- A) Case-insensitive `icontains` on name/code with indexes; Django Paginator; template highlighting

  - Pros
    - Works on SQLite/Postgres; easy to test; minimal setup
  - Cons
    - Not fuzzy; relevance basic
  - Notes
    - Enough for PRD

- B) Postgres trigram similarity

  - Pros
    - Better fuzzy matching
  - Cons
    - Postgres-only; more setup
  - Notes
    - Optional later path

---

## Decision

We choose A (`icontains` + pagination + highlight). URL design uses namespaced paths like `/search/?q=...`, `/airports/<code>/`, and reverse() everywhere. Canonical link and robots/sitemap configured for key pages.

Decision drivers ranked: portability, simplicity, SEO basics.

---

## Consequences

Positive

- Simple, deterministic search; portable across DBs
- Clean URL patterns and easy linking from templates

Negative and risks

- Less tolerant of typos compared to fuzzy search

Mitigations

- Add suggestions (starts-with ranking) or expose filter by country later

---

## Requirements binding

- FR-F-008-1 Search with pagination and highlighting (Trace F-008)
- FR-F-007-1 Templates share base layout; navbar search field (Trace F-007)
- NF-003 Security: templates autoescape; highlight safely

---

## Acceptance criteria snapshot

- AC: `GET /search/?q=LAX` paginates and highlights matches
- AC: Canonical URLs present on result pages; sitemap includes key views

Evidence to collect

- Test assertions on pagination HTML and highlight markup; view HTML snippet

---

## Implementation outline

Plan

- Implement `apps/search/views.py` with `q` parsing; guard empty queries
- Use Django Paginator; pass `page_obj` to templates; escape query
- Add simple highlight filter or method to wrap matches in `<mark>`

Denied paths

- No DB-specific trigram in MVP

Artifacts to update

- Search templates, navbar partial, sitemap/robots entries

---

## Test plan and invariants

Invariants

- INV-1 Pagination links preserve escaped query string
- INV-2 Highlighting does not break HTML escaping

Unit tests

- Tests for pagination, escaping, highlight; RequestFactory with templates asserted

Behavioral tests

- Visual checks of search page via script

---

## Documentation updates

- docs/ux/search-and-urls.md

---

## Rollback and contingency

Rollback trigger

- Performance or UX complaints

Rollback steps

- Switch to exact-match only or restrict to startswith

Data and config safety

- No data migrations

---

## Attestation plan

Human witness

- Reviewer validates HTML outputs and pagination behavior

Attestation record

- Commit hash and test outputs

---

## Checklist seed

- [ ] Paginator wired; links tested
- [ ] Highlight helper escapes correctly
- [ ] Canonical and sitemap configured

---

## References

- PRD §4 F-008; §10 Acceptance
