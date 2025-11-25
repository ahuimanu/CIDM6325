# ADR-1.0.18 Template cohesion from Bootstrap 5 examples

Date: 2025-11-16  
Status: Proposed  
Version: 1.0  
Authors: Course Staff  
Reviewers: TODO

---

## Links and traceability

PRD link: docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#4-scope-items-and-checklist-seeds (Scope) · docs/travelmathlite/prd/travelmathlite_prd_v1.0.0.md#10-acceptance-criteria (Acceptance)  
Related ADRs: ADR-1.0.17 UI stack (Bootstrap 5 + HTMX), ADR-1.0.4 Search strategy and URL design, ADR-1.0.15 Accessibility standards  
Source examples: `downloads/bootstrap-5.3.8-examples.zip` (official Bootstrap 5 examples)

---

## Intent and scope

Establish cohesive, repeatable template patterns across apps using stock Bootstrap 5 examples, minimizing custom CSS/JS. This ADR defines our base layout, component usage, and page scaffolds to ensure visual and interaction consistency.

In scope: base layout, navbar/footer, container/grid rules, standard components (cards/list groups/tables), forms, pagination, breadcrumbs, alerts, and utility classes.  
Out of scope: theming beyond Bootstrap defaults, custom CSS frameworks, design tokens outside Bootstrap variables.

---

## Problem and forces

- Current templates risk divergence across apps; we need consistent scaffolding and component choices.
- Forces: speed (use examples), consistency (shared partials), low maintenance (no custom CSS), accessibility (Bootstrap defaults), SEO blocks (canonical/meta) per ADR-1.0.4.
- Constraints: “100% Bootstrap” (no custom CSS besides optional variables inlined if absolutely needed), DB-agnostic views.

---

## Options considered

- A) Adopt official Bootstrap example patterns as-is (Album, Blog, Carousel, Dashboard, Headers/Footers, Heroes, Offcanvas, Pricing, Sign-in, Sticky footer, Sidebars, Navbars) and compose pages using only Bootstrap utilities/components.
  - Pros: fast, consistent, accessible; zero custom CSS; great docs; easy onboarding
  - Cons: generic look; limited brand differentiation
  - Notes: matches class constraints; reduces bikeshedding

- B) Introduce a custom theme (Bootswatch/custom variables) and bespoke components
  - Pros: differentiated look, finer control
  - Cons: more maintenance; risk of inconsistency; out-of-scope per “100% Bootstrap”

---

## Decision

Choose A. Standardize on patterns from the official examples with zero custom CSS. Use Bootstrap utilities and components only. Provide a cohesive component catalogue and page skeletons that all features reuse.

Key choices mapped to examples

- Layout: base from “Navbar” + “Sticky footer” examples; container default `.container` (switch to `.container-fluid` only for dashboards/maps).  
- Navbar: simple brand-left, right-aligned search form (GET to `/search/`) modeled on “Navbars” example; collapse on md.  
- Footer: sticky footer pattern with muted links.  
- Search results: use “List group” or “Cards (Album)” depending on density; default to `.list-group` for airports/cities; include `.pagination` from examples.  
- Forms: input groups for search and filters; validation states per Bootstrap.  
- Tables: use `.table` + `.table-striped` for tabular views; responsive wrapper `.table-responsive`.  
- Breadcrumbs: Bootstrap `.breadcrumb` when the page is nested.  
- Alerts: `.alert` for flash messages.  
- Offcanvas: not used by default (keep simple); allowed for secondary nav if needed.  
- Modals: avoid unless necessary; prefer inline patterns.  
- Highlight: use semantic `<mark>` (Bootstrap `.mark` style) per ADR-1.0.4.

SEO blocks (from ADR-1.0.4)

- Include canonical link block in `<head>`; results pages self-reference including `q`/`page`.

Accessibility and i18n

- Rely on Bootstrap’s accessible patterns; follow ADR-1.0.15 for specifics. Defer full i18n beyond string placement.

---

## Consequences

Positive

- Consistent look-and-feel with minimal effort; simpler reviews; faster template iteration.

Negative and risks

- Generic appearance; limited customization.

Mitigations

- Allow future ADR to introduce a light theme via variables if required; keep markup stable.

---

## Requirements binding

- FR-F-007-1 Cohesive base layout and navbar across apps  
- NF-003 Security: templates autoescape; use semantic `<mark>` for highlights  
- PRD §10 Acceptance: provide visual evidence using standardized pages

---

## Acceptance criteria snapshot

- AC: Base template provides navbar, canonical block, and sticky footer using only Bootstrap classes.  
- AC: Search results page composes list group + pagination without custom CSS.  
- AC: All app index pages adopt the same container/grid spacing and breadcrumbs when nested.

Evidence to collect

- Screenshots of base, search, and one additional app page following the catalogue.

---

## Implementation outline

Plan

- Create/align `apps/base/templates/base.html` with navbar (brand + search), main container, messages, footer.  
- Add partials under `apps/base/templates/partials/`: `_navbar.html`, `_footer.html`, `_messages.html`.  
- Update app templates to extend `base.html`; standardize sections: `title`, `meta`, `breadcrumbs`, `content`, `scripts`.  
- Provide snippet examples under `docs/ux/templates-bootstrap-catalogue.md` referencing Bootstrap examples used.

Denied paths

- No custom CSS or JS beyond Bootstrap bundle; no third-party themes.

Artifacts to update

- Base and app templates; docs catalogue; screenshots.

---

## Test plan and invariants

Invariants

- INV-TPL-1: No custom CSS files are introduced; only Bootstrap classes/utilities are used.  
- INV-TPL-2: Navbar search submits via GET to `search:index` and preserves `q` value.  
- INV-TPL-3: Pagination markup uses Bootstrap `.pagination` and preserves query string (ties to ADR-1.0.4 INV-1).

Unit/behavioral tests

- Template rendering tests for base and search pages; assert canonical link exists; assert navbar form target.  
- Visual checks via script capturing screenshots of base/search pages.

---

## Documentation updates

- Add `docs/ux/templates-bootstrap-catalogue.md` listing selected components and example links.  
- Reference `downloads/bootstrap-5.3.8-examples.zip` for reproduction.

---

## Rollback and contingency

Rollback trigger

- Need for stronger branding or unmet accessibility concerns.

Rollback steps

- Introduce a variables-based theme in a new ADR while preserving markup.

Data and config safety

- No data/config changes.

---

## Attestation plan

Human witness

- Reviewer validates base/search templates use only Bootstrap classes and follow catalogue.

Attestation record

- Commit hash, screenshots, and test outputs.

---

## Checklist seed

- [ ] Base layout and partials use only Bootstrap classes  
- [ ] Navbar search wired and preserves `q`  
- [ ] Pagination uses Bootstrap and keeps query string  
- [ ] Docs page added with component catalogue  
- [ ] Screenshots captured for base/search/app index

---

## References

- Bootstrap 5 examples (Album, Blog, Carousel, Dashboard, Headers/Footers, Heroes, Navbars, Offcanvas, Pricing, Sign-in, Sticky footer, Sidebars)  
- ADR-1.0.4 Search and URLs; ADR-1.0.15 Accessibility; ADR-1.0.17 UI stack
