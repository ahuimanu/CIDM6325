"""Visual regression check for search feature.

Captures screenshots of search flows for manual/automated visual inspection.
Run with: python scripts/visual_check_search.py (after: playwright install chromium)
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright


def wait_for_port(host: str, port: int, timeout: float = 25.0) -> bool:
    """Poll until the given port is listening or timeout expires."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.5)
            try:
                if sock.connect_ex((host, port)) == 0:
                    return True
            except OSError:
                pass
        time.sleep(0.25)
    return False


def main() -> int:
    # Project root is the travelmathlite folder containing manage.py
    project_root = Path(__file__).resolve().parents[1]
    manage_py = project_root / "manage.py"
    screenshots_dir = project_root / "screenshots" / "search"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    host = os.environ.get("VISUAL_CHECK_HOST", "127.0.0.1")
    port = int(os.environ.get("VISUAL_CHECK_PORT", "8010"))
    base_url = f"http://{host}:{port}"

    # Start Django dev server
    server = subprocess.Popen(
        [sys.executable, str(manage_py), "runserver", f"{host}:{port}"],
        cwd=str(project_root),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        if not wait_for_port(host, port, timeout=30):
            print("ERROR: Django dev server did not start in time.")
            try:
                outs, _ = server.communicate(timeout=1)
                if outs:
                    print(outs)
            except subprocess.TimeoutExpired:
                pass
            return 1

        print(f"✓ Django server ready at {base_url}")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            # Test 1: Empty search page
            print("Capturing: empty search page...")
            page.goto(f"{base_url}/search/")
            page.screenshot(path=str(screenshots_dir / "01-empty-search.png"))

            # Test 2: Search from navbar on home page
            print("Capturing: navbar search from home...")
            page.goto(f"{base_url}/")
            page.fill('input[name="q"]', "Dallas")
            page.screenshot(path=str(screenshots_dir / "02-navbar-search-filled.png"))
            page.click('button[type="submit"]')
            page.wait_for_url(f"{base_url}/search/?q=Dallas")
            page.screenshot(path=str(screenshots_dir / "03-search-results-dallas.png"))

            # Test 3: Pagination (if enough results)
            print("Capturing: search with pagination...")
            page.goto(f"{base_url}/search/?q=Airport")
            page.screenshot(path=str(screenshots_dir / "04-search-results-airport.png"))

            # Check if pagination exists and navigate to page 2
            if page.locator('a:has-text("2")').count() > 0:
                page.click('a:has-text("2")')
                page.wait_for_load_state("networkidle")
                page.screenshot(path=str(screenshots_dir / "05-search-results-page2.png"))

            browser.close()

        print(f"✓ Screenshots saved to {screenshots_dir}")
        return 0

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1

    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait()


if __name__ == "__main__":
    sys.exit(main())
