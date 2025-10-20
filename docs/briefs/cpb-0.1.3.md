# BRIEF (cpb-0.1.3): Feeds, Sitemap, and SEO Metadata

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §4 In Scope F-004; §5 FR-F-003-1/2; §10 Acceptance

ADR Anchor

- ADR-0.1.0 (Django MVP)

Goal

- Provide syndication (RSS + Atom), discoverability (sitemap.xml, robots.txt), and SEO metadata (canonical URLs, Open Graph/Twitter cards) for posts.

Bootstrap wireframes and blog structure

- Establish a consistent Bootstrap layout and navigation to serve as the baseline for SEO/meta additions:
  - Layout: `blog/base.html` uses Bootstrap 5 CDN, container, responsive navbar/footer, `{% block content %}` and `{% block extra_js %}`.
  - Navbar: Brand (Blog), links to Home (list), About, Projects, and Search form (GET) placeholder.
  - Post list: Card/list group layout with title, date, excerpt, and “Read more”.
  - Post detail: Article layout with title, date, tag list area (future), and sanitized Markdown body.
  - Forms: Use `.form-control`, `.btn`, spacing utilities; ensure consistent form group spacing.
  - Meta region: `<head>` space reserved for canonical and OG tags; ensure `{% block meta %}` can be extended.
  - Accessibility: Use proper heading order (h1 on page title) and nav landmarks.

Scope (single PR; ≲300 LOC)

- Feeds: Latest 10 published posts as RSS and Atom. Use Django syndication framework.
- Sitemap: Use Django sitemap framework for Post list + detail.
- robots.txt: Simple static response allowing crawling of site; disallow admin login page.
- Canonical URLs: Add a canonical link element on detail; ensure get_absolute_url on Post.
- Open Graph/Twitter: Inject title/description (excerpt) and canonical URL in base/detail templates.
- Tests: Verify feed endpoints 200 and contain post links; sitemap contains latest post; canonical tag present in detail.

Standards

- Python 3.12 + Django; PEP 8; type hints on new code.
- CBVs; sitemap/feeds via Django contrib frameworks.

Files to touch (anticipated)

- blog/models.py (add get_absolute_url)
- blog/feeds.py (new)
- blog/sitemaps.py (new)
- blog/urls.py (add feed/sitemap routes)
- myblog/urls.py (include sitemap/robots)
- blog/templates/blog/post_detail.html and base.html (wireframe polish + meta tags)
- blog/tests.py (new tests for feeds/sitemap/canonical)

Migration plan

- None (model method only).

Rollback

- Use git revert with the merge commit SHA to remove routes/files; no DB changes.

Acceptance

- GET /blog/feeds/rss/ and /blog/feeds/atom/ return latest 10 published posts.
- GET /sitemap.xml lists index + recent posts; robots.txt served.
- Detail pages include canonical and Open Graph meta tags.

How to Test (local)

1) py manage.py runserver
2) Visit /blog/feeds/rss/ and /blog/feeds/atom/
3) Visit /sitemap.xml and /robots.txt
4) Open a post detail; View Source for canonical/Open Graph tags
5) Run tests: py manage.py test blog -v 2

Prompts for Copilot

- Add get_absolute_url to Post; implement feeds.RSSFeed/AtomFeed using Django syndication.
- Add sitemaps.PostSitemap and wire in project urls.
- Add canonical and OG tags to templates; ensure context has absolute URL.
- Write tests for feeds, sitemap, and canonical tag presence.
