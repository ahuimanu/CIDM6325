# Playwright visual check (screenshots)

This helper launches the Django dev server and captures full-page screenshots of key pages for quick design review.

- Script: `blog_site/scripts/visual_check.py`
- Outputs: `blog_site/screenshots/`
- Default host/port: `127.0.0.1:8009`

## Prerequisites

- Virtual environment activated
- Python Playwright installed (already pinned in `requirements.txt`)
- One-time browser download:

```bash
python -m playwright install chromium
```

## Run

```bash
python blog_site/scripts/visual_check.py
```

This will generate:

- `blog_site/screenshots/blog_list.png` (full page)
- `blog_site/screenshots/post_form.png` (full page)
- `blog_site/screenshots/blog_list_vp.png` (viewport only)
- `blog_site/screenshots/post_form_vp.png` (viewport only)
- Timestamped copies in `blog_site/screenshots/history/` (e.g., `blog_list_YYYYmmdd_HHMMSS.png`)

## Configuration

Optional environment variables:

- `VISUAL_CHECK_HOST` (default `127.0.0.1`)
- `VISUAL_CHECK_PORT` (default `8009`)

Example:

```bash
VISUAL_CHECK_PORT=8010 python blog_site/scripts/visual_check.py
```

## Extending

Want more views? Add steps in `visual_check.py` to visit and screenshot:

- Post detail pages
- Delete confirm
- Mobile and desktop variants (e.g., 390x844 and 1440x900) via different `new_context(viewport=...)`
- A short flow (e.g., create a post then screenshot its detail)

If you tell me which pages to include, I’ll wire them in and re-run the captures.
