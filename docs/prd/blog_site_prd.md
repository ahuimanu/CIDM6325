# Product Requirements Document (PRD)

## 1. Document Information

- Product/Feature Name: Django Personal Blog Example
- Author(s): ahuimanu
- Date Created: 2025-10-07
- Last Updated: 2025-10-07
- Version: 0.1 (Draft)

---

## 2. Overview

Summary:  
A minimalist, production-quality Django blog application demonstrating modern best practices,
clean architecture, and static-friendly deployment. Serves as a living teaching artifact for
students learning Django fundamentals, content models, and deployment pipelines.

Problem Statement:  
Students need a concrete, maintainable example beyond trivial tutorials. Many examples are either
too small (polls) or too complex. This project fills the gap with a clean, real-world blog that
uses current Django conventions and a disciplined structure suitable for teaching.

Goals & Objectives:
- Deliver a working Django site with production-quality structure.
- Showcase reusable app patterns, settings organization, and content models.
- Provide a clear migration and deployment example (SQLite to Postgres).
- Demonstrate Markdown rendering and code syntax highlighting.
- Serve as an anchor project for Django pedagogy.

Non-Goals:
- Multi-user editorial workflows and permissions beyond a single author.
- Rich WYSIWYG editors or heavy front-end frameworks.
- Multi-tenant, API-first, or headless CMS behavior.

---

## 3. Context & Background

Business Context:  
Used in CIDM 6325 as a capstone-level Django example under the AI + Web Engineering track.

Market/Customer Insights:  
Students often grasp Django in theory but struggle with project structure. This example adopts
a lean, comprehensible pattern modeled after Carlton Gibson’s site to bridge theory and practice.

Competitive/Benchmark References:  
- Carlton Gibson’s site for tone and structure: <https://noumenal.es/>
- Provenance note for teaching reference: Matt Layman’s independently authored
  *Understand Django* at <https://www.mattlayman.com/understand-django/>
  (not affiliated with the Django Software Foundation; cited for educational use)

---

## 4. Scope

In Scope:
- Post model with slug, title, body (Markdown), publish date, tags.
- Static pages (About, Teaching, Projects).
- RSS and Atom feeds for posts.
- Code syntax highlighting.
- Sitemap, canonical URLs, SEO metadata.
- Search by title and content.
- Responsive CSS via a minimal framework (e.g., Tailwind or PicoCSS).
- Minimal admin for creating and editing posts.
- Deployment example (Docker, Gunicorn, Whitenoise).

Out of Scope:
- Multi-author accounts and editorial approval workflows.
- Commenting system.
- Personalization, recommendations, or complex analytics.
- External CMS integrations.

---

## 5. User Stories & Use Cases

Primary User Persona(s):  
Solo technical author and students studying Django.

User Stories:
- As a visitor, I want to browse posts chronologically and by tag so I can find topics of interest.
- As the author, I can write posts in Markdown and preview rendering before publishing.
- As a student, I can clone, run, and understand the architecture quickly.
- As a developer, I can fork this as a starter for my personal blog.

Use Case Scenarios:
- Happy path: Author creates a post in admin, saves, and the post appears on the home page and feeds.
- Edge case: Slug collision is resolved automatically with a suffix while preserving canonical URL rules.
- Edge case: Malformed Markdown is rendered safely with sanitization and graceful fallback.

---

## 6. Functional Requirements

- FR-001: Create, edit, and delete posts via Django admin.
- FR-002: Render Markdown with syntax highlighting and safe HTML sanitization.
- FR-003: Provide RSS and Atom feeds listing the latest 10 posts.
- FR-004: Generate canonical URLs using date and slug, and expose Open Graph meta tags.
- FR-005: Full-text search across titles and bodies with pagination of results.
- FR-006: Static pages for About and Projects served from templates or flatpages.
- FR-007: Generate XML sitemap and robots.txt.
- FR-008: Paginate the home page and tag archives.
- FR-009: Include unit tests for models, views, feeds, and URL resolution.

---

## 7. Non-Functional Requirements

- Performance: p95 response under 200 ms on a small container without cache.
- Scalability: Up to 5 k visits per day without a CDN; easy path to add cache and CDN later.
- Accessibility: WCAG 2.1 AA, keyboard navigation, focus states, and adequate contrast.
- Security/Compliance: CSRF, XSS-safe Markdown, limited HTML whitelist, secure headers.
- Reliability/Availability: 99.5 percent target with static asset fallback if DB unavailable.

---

## 8. Dependencies

- Internal: Django 5.x, django-taggit, markdown-it-py, Pygments, Whitenoise.
- External: SQLite for local, Postgres for production, Docker, GitHub Actions for CI.
- Cross-team: None expected; this is a standalone teaching example.

---

## 9. Risks & Assumptions

Risks:
- Unsafe Markdown or HTML could introduce XSS if sanitization is misconfigured.
- Student deployments may omit collectstatic and whitenoise configuration.
- Feed and SEO templates can drift as Django versions evolve.

Assumptions:
- Single author model is sufficient for the teaching goal.
- Python 3.12 or newer and Django 5.x are standard in the course environment.
- Hosting uses a simple container and object storage for static files if needed.

---

## 10. Acceptance Criteria

- FR-001 to FR-009 have passing unit tests and manual checks.
- Markdown posts render correctly with syntax highlighting and safe HTML.
- RSS and Atom feeds validate with standard validators.
- Sitemap and robots.txt are reachable and correct.
- Search returns relevant results within 100 ms for a 500 post dataset on a small container.
- CI runs linting for Python and Markdown and blocks on failure.

---

## 11. Success Metrics

- Setup time under 10 minutes for a student to run locally and create a first post.
- At least 90 percent of students report the architecture is understandable.
- Error rate under 1 percent in production logs across typical classroom usage.
- Test coverage of core app at or above 90 percent.

---

## 12. Rollout & Release Plan

Phasing:
- MVP v0.1: Post model, admin authoring, basic templates, Markdown, pagination.
- v0.2: Search, syntax highlighting, and tag archives.
- v0.3: RSS and Atom feeds, sitemap, robots.txt, SEO meta, canonical links.
- v1.0: Hardened deployment docs, accessibility review, and test coverage target met.

Release Channels:
- Public GitHub repository and course module bundle.

Training/Documentation Needs:
- README with setup, run, and deploy steps.
- Architecture overview in docs describing apps, models, URLs, and templates.
- Short tutorial: Build your own blog in Django 5.x.

---

## 13. Open Questions

- Should Markdown live in the database only or support optional filesystem import for drafts.
- Should a minimal JSON API be included for future Jamstack or mobile clients.
- Preferred CSS pipeline: Tailwind via CLI build or a no-build CSS framework.

---

## 14. References

- Carlton Gibson’s site: <https://noumenal.es/>
- Matt Layman, *Understand Django* (independently authored teaching resource):
  <https://www.mattlayman.com/understand-django/>
- Django 5.0 documentation: <https://docs.djangoproject.com/en/5.0/>
- markdown-it-py: <https://markdown-it-py.readthedocs.io/>
- django-taggit: <https://django-taggit.readthedocs.io/>