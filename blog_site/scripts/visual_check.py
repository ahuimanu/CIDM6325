import os
import socket
import subprocess
import sys
import time
from contextlib import closing
from pathlib import Path

from playwright.sync_api import sync_playwright


def wait_for_port(host: str, port: int, timeout: float = 25.0) -> bool:
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
    # Project root is the Django project folder containing manage.py
    project_root = Path(__file__).resolve().parents[1]
    manage_py = project_root / "manage.py"

    host = os.environ.get("VISUAL_CHECK_HOST", "127.0.0.1")
    port = int(os.environ.get("VISUAL_CHECK_PORT", "8009"))
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
            # Print any captured server output to help diagnose
            try:
                outs, _ = server.communicate(timeout=1)
                print(outs)
            except Exception:
                pass
            return 1

        out_dir = project_root / "screenshots"
        out_dir.mkdir(exist_ok=True)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()

            ts = time.strftime("%Y%m%d_%H%M%S")
            history_dir = out_dir / "history"
            history_dir.mkdir(exist_ok=True)

            # 1) Blog list page (cache-busted) — capture full-page and viewport variants
            page.goto(f"{base_url}/blog/?_ts={ts}", wait_until="networkidle")
            page.screenshot(path=str(out_dir / "blog_list.png"), full_page=True)
            page.screenshot(path=str(out_dir / "blog_list_vp.png"), full_page=False)
            page.screenshot(path=str(history_dir / f"blog_list_{ts}.png"), full_page=False)

            # 2) New post form (cache-busted); no submit to avoid editor complexities
            page.goto(f"{base_url}/blog/post/new/?_ts={ts}", wait_until="networkidle")
            page.screenshot(path=str(out_dir / "post_form.png"), full_page=True)
            page.screenshot(path=str(out_dir / "post_form_vp.png"), full_page=False)
            page.screenshot(path=str(history_dir / f"post_form_{ts}.png"), full_page=False)

            # 3) Perform a search via the navbar and capture results
            search_query = os.environ.get("VISUAL_CHECK_SEARCH_QUERY", "fun")
            page.goto(f"{base_url}/blog/?_ts={ts}", wait_until="networkidle")
            # Fill the search input in the navbar and submit
            page.fill('input[name="q"]', search_query)
            page.click('form[role="search"] button[type="submit"]')
            page.wait_for_load_state("networkidle")
            # Also wait for the Search header to ensure results page is rendered
            try:
                page.wait_for_selector('h1:has-text("Search")', timeout=3000)
            except Exception:
                pass
            page.screenshot(path=str(out_dir / "search_results.png"), full_page=True)
            page.screenshot(path=str(out_dir / "search_results_vp.png"), full_page=False)
            page.screenshot(path=str(history_dir / f"search_results_{ts}.png"), full_page=False)

            context.close()
            browser.close()

        print(f"Saved screenshots to: {out_dir}")
        return 0
    finally:
        # Gracefully stop server
        try:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
