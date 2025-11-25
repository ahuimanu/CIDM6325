# BRIEF (cpb-0.1.7): Visual checks with Playwright (screenshots)

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §10 Acceptance (UI quality and verification)

ADR Anchor

- ADR-0.1.0 (Django MVP)

Goal

- Add a fast, repeatable way to capture full-page screenshots of key blog views to accelerate design review and iterate on Bootstrap layout.

Scope (single PR; ≤300 LOC)

- Use Playwright for Python to automate a headless Chromium session that:
  - Starts the Django dev server
  - Visits /blog/ (list) and /blog/post/new/ (form)
  - Saves screenshots under `blog_site/screenshots/`
- Provide script-local docs and a top-level README pointer.
- Keep tests unchanged (Django TestCase only); this is a developer tool, not a test framework migration.

Standards

- Python 3.12+; PEP 8; type hints on new code.
- No pytest introduction; keep Django TestCase for unit/functional tests.
- Conventional commits.

Files to touch (anticipated)

- blog_site/scripts/visual_check.py (new): launch server + capture screenshots
- blog_site/screenshots/ (new): output directory
- blog_site/scripts/README.md (new): usage, env vars, extension notes
- README.MD (update): short "Visual check" section linking to the script
- requirements.txt (add playwright pinned)

Acceptance

- Running `python blog_site/scripts/visual_check.py` from repo root:
  - Launches dev server on 127.0.0.1:8009
  - Creates `blog_site/screenshots/blog_list.png` and `blog_site/screenshots/post_form.png`
  - Shuts down server cleanly
- A one-time `python -m playwright install chromium` is documented.

How to Use (local)

```bash
# one-time browser install
python -m playwright install chromium

# capture screenshots
python blog_site/scripts/visual_check.py
```

Prompts for Copilot

- "Create a Python script using Playwright to start Django (manage.py runserver), wait for the port, visit /blog/ and /blog/post/new/, screen-cap to blog_site/screenshots/, then terminate."
- "Extend the script to capture post detail and mobile viewport (390x844)."
- "Add a README next to the script and a short section in the root README."
