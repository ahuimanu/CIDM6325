#!/usr/bin/env python3
"""Simple Playwright visual check for static pipeline.

This script launches a browser, loads `/` on the running site (default
`http://localhost:8000`), captures a screenshot into
`travelmathlite/screenshots/static-pipeline/` and writes a small `links-*.txt`
file listing stylesheet/script `href`/`src` values discovered on the page.

Usage:
  uv run python travelmathlite/scripts/visual_checks/static_pipeline_check.py \
    --url http://localhost:8000 --out-dir travelmathlite/screenshots/static-pipeline

Requires Playwright Python to be installed and browsers to be installed via
`playwright install`.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path


def make_parser():
    p = argparse.ArgumentParser(description="Capture screenshot and static links from /")
    p.add_argument("--url", default="http://localhost:8000", help="Base URL to load")
    p.add_argument("--out-dir", default=Path("travelmathlite/screenshots/static-pipeline"), type=Path)
    p.add_argument("--headless", action="store_true", help="Run headless (default: headful for debugging)")
    return p


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = make_parser()
    ns = parser.parse_args(argv)

    out_dir: Path = ns.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    screenshot_path = out_dir / f"static-pipeline-{ts}.png"
    links_path = out_dir / f"links-{ts}.txt"

    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        print("Playwright is required: pip install playwright && playwright install")
        raise

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=ns.headless)
        page = browser.new_page()
        page.goto(ns.url)
        page.wait_for_load_state("networkidle")

        # collect stylesheet hrefs and script srcs that look like static assets
        links = []
        for el in page.query_selector_all("link[rel=stylesheet]"):
            href = el.get_attribute("href")
            if href:
                links.append(href)
        for el in page.query_selector_all("script[src]"):
            src = el.get_attribute("src")
            if src:
                links.append(src)

        page.screenshot(path=str(screenshot_path), full_page=True)
        browser.close()

    with links_path.open("w", encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

    print(f"Wrote screenshot: {screenshot_path}")
    print(f"Wrote links file: {links_path}")


if __name__ == "__main__":
    raise SystemExit(main())
