"""Visual regression check for HTMX calculator features.

Captures screenshots of HTMX-enhanced calculator flows for manual/automated visual inspection.
Tests both HTMX partial updates and full-page fallback behavior.

Run with: uvx playwright install chromium && python scripts/visual_check_htmx_calculators.py
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
    screenshots_dir = project_root / "screenshots" / "calculators"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    host = os.environ.get("VISUAL_CHECK_HOST", "127.0.0.1")
    port = int(os.environ.get("VISUAL_CHECK_PORT", "8011"))
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

            # Test 1: Distance calculator with HTMX enabled
            print("\n=== Testing Distance Calculator with HTMX ===")
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            print("Capturing: empty distance calculator...")
            page.goto(f"{base_url}/calculators/distance/")
            page.screenshot(path=str(screenshots_dir / "01-distance-empty.png"))

            print("Capturing: distance calculator form filled...")
            page.fill('input[name="origin"]', "35.2194,-101.7059")
            page.fill('input[name="destination"]', "32.8968,-97.0380")
            page.screenshot(path=str(screenshots_dir / "02-distance-filled.png"))

            print("Capturing: distance calculator HTMX result...")
            page.click('button[type="submit"]')
            # Wait for HTMX swap to complete
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshots_dir / "03-distance-htmx-result.png"))

            # Test 2: Distance calculator validation error with HTMX
            print("Capturing: distance calculator validation error...")
            page.goto(f"{base_url}/calculators/distance/")
            page.fill('input[name="origin"]', "")
            page.fill('input[name="destination"]', "32.8968,-97.0380")
            page.click('button[type="submit"]')
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshots_dir / "04-distance-validation-error.png"))

            page.close()

            # Test 3: Cost calculator with HTMX enabled
            print("\n=== Testing Cost Calculator with HTMX ===")
            page = browser.new_page(viewport={"width": 1280, "height": 800})

            print("Capturing: empty cost calculator...")
            page.goto(f"{base_url}/calculators/cost/")
            page.screenshot(path=str(screenshots_dir / "05-cost-empty.png"))

            print("Capturing: cost calculator form filled...")
            page.fill('input[name="origin"]', "35.2194,-101.7059")
            page.fill('input[name="destination"]', "32.8968,-97.0380")
            page.fill('input[name="fuel_economy_l_per_100km"]', "8.0")
            page.fill('input[name="fuel_price_per_liter"]', "1.50")
            page.screenshot(path=str(screenshots_dir / "06-cost-filled.png"))

            print("Capturing: cost calculator HTMX result...")
            page.click('button[type="submit"]')
            # Wait for HTMX swap to complete
            page.wait_for_timeout(2000)
            page.screenshot(path=str(screenshots_dir / "07-cost-htmx-result.png"))

            page.close()

            # Test 4: Verify fallback (no JavaScript)
            print("\n=== Testing Fallback Without JavaScript ===")
            context = browser.new_context(java_script_enabled=False, viewport={"width": 1280, "height": 800})
            page = context.new_page()

            print("Capturing: distance calculator without JS (initial)...")
            page.goto(f"{base_url}/calculators/distance/")
            page.screenshot(path=str(screenshots_dir / "08-distance-no-js-empty.png"))

            print("Capturing: distance calculator without JS (filled)...")
            page.fill('input[name="origin"]', "35.2194,-101.7059")
            page.fill('input[name="destination"]', "32.8968,-97.0380")
            page.screenshot(path=str(screenshots_dir / "09-distance-no-js-filled.png"))

            print("Capturing: distance calculator without JS (result - full page reload)...")
            page.click('button[type="submit"]')
            # Wait for page load (full page reload without HTMX)
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1000)
            page.screenshot(path=str(screenshots_dir / "10-distance-no-js-result.png"))

            context.close()
            browser.close()

        print(f"\n✓ All screenshots saved to {screenshots_dir}")
        print("\nScreenshots captured:")
        print("  - Distance calculator: empty, filled, HTMX result, validation error")
        print("  - Cost calculator: empty, filled, HTMX result")
        print("  - No-JS fallback: empty, filled, full page result")

        return 0

    finally:
        # Clean shutdown of Django server
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    sys.exit(main())
