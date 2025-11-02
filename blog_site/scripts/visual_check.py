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

            # 1) Blog list page
            page.goto(f"{base_url}/blog/", wait_until="networkidle")
            page.screenshot(path=str(out_dir / "blog_list.png"), full_page=True)

            # 2) New post form (no submit to avoid editor scripting complexities)
            page.goto(f"{base_url}/blog/post/new/", wait_until="networkidle")
            page.screenshot(path=str(out_dir / "post_form.png"), full_page=True)

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
