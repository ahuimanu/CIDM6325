# Product Requirements Document (PRD)

## 1. Document Information

- Product/Feature Name: Django Personal Blog Example  
- Author(s): ahuimanu  
- Date Created: 2025-10-13  
- Last Updated: 2025-10-13  
- Version: 1.0.1 (Draft)

---

## 2. Overview

### **Summary**  

A minimalist, production-quality Django blog application demonstrating modern best practices,
clean architecture, and static-friendly deployment. Serves as a living teaching artifact for
students learning Django fundamentals, content models, and deployment pipelines.

### **Problem Statement**  

Students need a concrete, maintainable example beyond trivial tutorials. Many examples are either
too small (polls) or too complex. This project fills the gap with a clean, real-world blog that
uses current Django conventions and a disciplined structure suitable for teaching.

### **Goals & Objectives**

- Deliver a working Django site with production-quality structure.  
- Showcase reusable app patterns, settings organization, and content models.  
- Provide a clear migration and deployment example (SQLite → Postgres).  
- Demonstrate Markdown rendering and code syntax highlighting.  
- Serve as an anchor project for Django pedagogy.

### **Non-Goals**

- Multi-user editorial workflows and permissions beyond a single author.  
- Rich WYSIWYG editors or heavy front-end frameworks.  
- Multi-tenant, API-first, or headless CMS behavior.

---

## 3. Context & Background

**Business Context**  
Used in CIDM 6325 as a capstone-level Django example under the AI + Web Engineering track.

**Market/Customer Insights**  
Students often grasp Django in theory but struggle with project structure. This example adopts
a lean, comprehensible pattern modeled after Carlton Gibson’s site to bridge theory and practice.

**Competitive/Benchmark References**  

- Carlton Gibson’s site for tone and structure: <https://noumenal.es/>  
- Provenance note for teaching reference: Matt Layman’s *Understand Django*
  <https://www.mattlayman.com/understand-django/>

---

## 4. Scope (Checklist Seeds)

> This section defines all in-scope capabilities as **checklistable items**.  
> Each bullet must later appear in a deliverable checklist (see Section 6).

### In Scope

- [ ] **F-001 Post Model** — Slug, title, body (Markdown), publish date, tags.  
  Acceptance: CRUD operations functional, slugs unique, Markdown renders safely.  
  Trace: FR-001, FR-002.
- [ ] **F-002 Admin Authoring** — Create/edit posts in Django Admin.  
  Acceptance: Accessible only to staff, slug pre-populated, list view shows title/date.  
  Trace: FR-001.
- [ ] **F-003 Markdown Rendering** — Safe HTML sanitization and syntax highlighting.  
  Acceptance: Markdown renders via markdown-it-py and pygments; no unsafe tags.  
  Trace: FR-002.
- [ ] **F-004 Feeds and SEO** — RSS, Atom, sitemap, canonical URLs, Open Graph tags.  
  Acceptance: Feeds validate, sitemap lists core URLs, SEO metadata correct.  
  Trace: FR-003, FR-004, FR-007.
- [ ] **F-005 Search** — Full-text search on title and body with pagination.  
  Acceptance: Search returns relevant posts in under 100 ms for 500-post dataset.  
  Trace: FR-005.
- [ ] **F-006 Static Pages** — About, Teaching, Projects templates.  
  Acceptance: Pages render through Django templates or FlatPages app.  
  Trace: FR-006.
- [ ] **F-007 Responsive Styling** — Lightweight CSS (Tailwind or PicoCSS).  
  Acceptance: Layout responsive across desktop/mobile, color contrast meets AA.  
  Trace: NF-002.
- [ ] **F-008 Deployment Example** — Docker, Gunicorn, Whitenoise.  
  Acceptance: App deploys locally and remotely with identical configuration.  
  Trace: OPS-004.

### Out of Scope

- Multi-author editorial features.  
- Commenting, analytics, personalization.  
- External CMS or REST API integrations.

---

## 5. Functional Requirements (Bound to Scope)

> Each FR must trace back to an F-ID from Section 4 and later appear in the generated checklist.

- **FR-F-001-1:** Create, edit, and delete posts via Django admin. → Trace F-001, F-002  
- **FR-F-001-2:** Ensure slug uniqueness and canonical URLs. → Trace F-001, F-004  
- **FR-F-002-1:** Render Markdown safely with syntax highlighting. → Trace F-003  
- **FR-F-002-2:** Sanitize unsafe HTML tags and attributes. → Trace F-003  
- **FR-F-003-1:** Provide RSS and Atom feeds for latest 10 posts. → Trace F-004  
- **FR-F-003-2:** Generate XML sitemap and robots.txt. → Trace F-004  
- **FR-F-004-1:** Implement search over titles and bodies. → Trace F-005  
- **FR-F-005-1:** Serve static “About” and “Projects” pages. → Trace F-006  
- **FR-F-006-1:** Ensure pagination on index and tag views. → Trace F-001, F-005  
- **FR-F-007-1:** Include automated tests for all views and feeds. → Trace F-001 – F-005.

---

## 6. Checklist Generation Expectation

> Upon PRD sign-off, a feature checklist must be generated directly from Section 4 and 5.  
> The checklist will include:
>
> - [ ] Completion box per F-ID  
> - User story summary  
> - Acceptance criteria bullets  
> - Linked artifacts or PR references  
> - Test status and Gate 5 attestation  
>
> Saved as `docs/checklists/blog_site_feature_checklist.md`

---

## 7. Non-Functional Requirements

- **Performance:** p95 < 200 ms responses on a small container.  
- **Scalability:** Handles ≥ 5 000 visits per day without cache.  
- **Accessibility:** WCAG 2.1 AA contrast and keyboard nav.  
- **Security/Compliance:** CSRF, sanitized Markdown, secure headers.  
- **Reliability:** 99.5 % uptime with static fallback.

---

## 8. Dependencies

- **Internal:** Django 5.x, django-taggit, markdown-it-py, Pygments, Whitenoise  
- **External:** SQLite (local), Postgres (prod), Docker, GitHub Actions  
- **Cross-Team:** None (expected standalone teaching example)

---

## 9. Risks & Assumptions

### **Risks**

- Misconfigured sanitization may permit XSS.  
- Students may skip collectstatic setup.  
- Feed templates can drift with Django upgrades.

### **Assumptions**

- Single-author model sufficient.  
- Python 3.12 + Django 5.x baseline.  
- Simple container hosting with object storage for static files.

---

## 10. Acceptance Criteria

- All FR-F-### requirements pass tests and manual checks.  
- Markdown posts render correctly and safely.  
- Feeds validate per RSS/Atom standards.  
- Sitemap and robots.txt reachable and correct.  
- Search returns accurate results within target latency.  
- CI blocks on lint/test failures.

---

## 11. Success Metrics

- Setup time < 10 minutes for students.  
- ≥ 90 % students report architecture understandable.  
- Production error rate < 1 %.  
- Core test coverage ≥ 90 %.

---

## 12. Rollout & Release Plan

**Phasing**  

- v0.1 MVP — Post model, admin, templates, Markdown, pagination.  
- v0.2 — Search and syntax highlighting.  
- v0.3 — Feeds, sitemap, SEO, canonical links.  
- v0.4 — Docs, accessibility, full coverage.

**Release Channels**  

- Public GitHub repo and WTAMU course module.  

**Training/Documentation**  

- README, architecture overview, short tutorial (*Build Your Own Blog in Django 5.x*).

---

## 13. Open Questions

- Store Markdown only in DB or support filesystem drafts?  
- Include minimal JSON API for Jamstack clients?  A: HTMX
- Tailwind CLI vs no-build CSS framework? A: Bootstrap

---

## 14. References

- Carlton Gibson site [https://noumenal.es/](https://noumenal.es/)
- Matt Layman *Understand Django* <https://www.mattlayman.com/understand-django/>  
- Django 5.0 Docs <https://docs.djangoproject.com/en/5.0/>  
- markdown-it-py <https://markdown-it-py.readthedocs.io/>  
- django-taggit <https://django-taggit.readthedocs.io/>
