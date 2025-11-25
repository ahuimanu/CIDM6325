#!/usr/bin/env python3
"""Run Django collectstatic with logging and summary generation.

Usage:
  uv run python scripts/run_collectstatic.py [--dry-run] [--clear] [--noinput] \
      [--settings DJANGO_SETTINGS_MODULE] [--log-dir PATH] [--archive-logs]

The script will ensure `DJANGO_SETTINGS_MODULE` is set (can be overridden via
`--settings`). It calls Django's `call_command('collectstatic', ...)` in-process
so the project's settings are used. Output is written to a timestamped log file
under `docs/travelmathlite/ops/logs/` by default and a concise summary markdown
is emitted next to the log.

This file intentionally avoids external dependencies and uses the stdlib.
"""

from __future__ import annotations

import argparse
import datetime
import io
import os
import sys
import tarfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

# Default to the repository-root docs folder so logs land in a stable location
# regardless of the current working directory when the script is invoked.
SCRIPT_DIR = Path(__file__).resolve().parent
# travelmathlite/scripts -> parents[1] == repo root (CIDM6325)
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_LOG_DIR = REPO_ROOT / "docs" / "travelmathlite" / "ops" / "logs"


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run Django collectstatic with logs")
    p.add_argument("--dry-run", action="store_true", help="Pass --dry-run to collectstatic")
    p.add_argument("--clear", action="store_true", help="Pass --clear to collectstatic")
    p.add_argument("--noinput", action="store_true", help="Pass --noinput to collectstatic")
    p.add_argument("--settings", type=str, help="DJANGO_SETTINGS_MODULE to use")
    p.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR, help="Directory to write logs")
    p.add_argument("--archive-logs", action="store_true", help="Create a .tar.gz archive of the logs after run")
    return p


def ensure_logs_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_log_and_summary(log_dir: Path, base_name: str, stdout_text: str, stderr_text: str, settings_module: str | None) -> int:
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d-%H%M%S")
    log_file = log_dir / f"collectstatic-{base_name}-{ts}.log"
    summary_file = log_dir / f"collectstatic-summary-{base_name}-{ts}.md"

    with log_file.open("w", encoding="utf-8") as f:
        f.write("=== STDOUT ===\n")
        f.write(stdout_text)
        f.write("\n=== STDERR ===\n")
        f.write(stderr_text)

    # attempt to locate STATIC_ROOT and manifest
    manifest_present = False
    files_copied = None
    try:
        # import settings after django.setup()
        from django.conf import settings

        static_root = Path(settings.STATIC_ROOT) if settings.STATIC_ROOT else None
        if static_root and static_root.exists():
            manifest_path = static_root / "staticfiles.json"
            manifest_present = manifest_path.exists()
            # count files in STATIC_ROOT for a basic metric
            files_copied = sum(1 for _ in static_root.rglob("*") if _.is_file())
    except Exception:
        static_root = None

    with summary_file.open("w", encoding="utf-8") as f:
        f.write(f"# collectstatic summary ({ts})\n\n")
        f.write(f"- Command base: `{base_name}`\n")
        if settings_module:
            f.write(f"- DJANGO_SETTINGS_MODULE: `{settings_module}`\n")
        if static_root:
            f.write(f"- STATIC_ROOT: `{static_root}`\n")
        f.write(f"- Manifest present: `{manifest_present}`\n")
        if files_copied is not None:
            f.write(f"- Files under STATIC_ROOT: `{files_copied}`\n")
        f.write("\n\nSee the full log: `" + str(log_file) + "`\n")

    print(f"Wrote log: {log_file}")
    print(f"Wrote summary: {summary_file}")
    return 0 if (manifest_present or files_copied is not None) else 2


def archive_logs(log_dir: Path, pattern: str = "collectstatic-*.log") -> Path:
    ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d-%H%M%S")
    archive_path = log_dir / f"collectstatic-logs-{ts}.tar.gz"
    with tarfile.open(archive_path, "w:gz") as tar:
        for p in sorted(log_dir.glob(pattern)):
            tar.add(p, arcname=p.name)
    print(f"Created archive: {archive_path}")
    return archive_path


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = make_parser()
    ns = parser.parse_args(argv)

    # ensure log dir exists
    log_dir: Path = ns.log_dir
    ensure_logs_dir(log_dir)

    # if settings provided, export it
    settings_module = None
    if ns.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = ns.settings
        settings_module = ns.settings
    elif os.environ.get("DJANGO_SETTINGS_MODULE"):
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")

    # prepare call_command args
    cmd_args = []
    if ns.dry_run:
        cmd_args.append("--dry-run")
    if ns.clear:
        cmd_args.append("--clear")
    if ns.noinput:
        cmd_args.append("--noinput")

    # capture output
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    try:
        # import and setup django
        import django

        django.setup()
        from django.core.management import call_command

        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            call_command("collectstatic", *cmd_args)

    except SystemExit as se:
        # django's call_command may call sys.exit()
        stderr_buf.write(f"SystemExit: {se}\n")
    except Exception as exc:
        stderr_buf.write(f"Exception while running collectstatic: {exc}\n")

    stdout_text = stdout_buf.getvalue()
    stderr_text = stderr_buf.getvalue()

    # write logs and summary
    ret = write_log_and_summary(log_dir, "run", stdout_text, stderr_text, settings_module)

    if ns.archive_logs:
        archive_logs(log_dir)

    # return 0 on success, else non-zero
    return ret


if __name__ == "__main__":
    raise SystemExit(main())
