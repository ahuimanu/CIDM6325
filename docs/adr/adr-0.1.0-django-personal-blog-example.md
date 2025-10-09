# ADR-0.1.0: Adopt Django for Personal Blog Example MVP

Date: 2025-10-07  
Status: Proposed

---

## Context

- PRD link: [docs/blog_site_prd.md](../blog_site_prd.md) §2, §4
- Problem/forces:  
  Need a maintainable, production-quality blog example for CIDM 6325 students. Must demonstrate modern Django best practices, clean architecture, and static-friendly deployment. Should be simple enough for teaching, but robust enough for real-world use.

---

## Options

- **A) Django 5.x (single app, CBVs, admin, Markdown, SQLite/Postgres)**
- **B) Flask or FastAPI (minimal blog, custom admin, Markdown, SQLite/Postgres)**
- **C) Static site generator (e.g., Hugo, Jekyll) with Markdown posts**

---

## Decision

We choose **A) Django 5.x** because:
- Django is the course focus and aligns with student learning goals.
- Built-in admin, ORM, and CBVs support rapid development and clean architecture.
- Ecosystem supports Markdown, syntax highlighting, tagging, feeds, and static deployment.
- Proven patterns for migration, deployment, and testing.

---

## Consequences

**Positive:**
- Students learn idiomatic Django project/app structure.
- Easy to extend with tags, feeds, and static pages.
- Leverages Django admin for authoring, reducing custom code.

**Negative/Risks:**
- Django’s learning curve for CBVs and settings management.
- Markdown sanitization must be handled securely.
- Static deployment (Whitenoise, collectstatic) may require extra setup.

---

## Validation

- Acceptance: MVP delivers post CRUD, Markdown rendering, pagination, and basic templates (see PRD §6, §10).
- Rollback: If Django proves too complex, fallback to a static generator or simpler Flask app.