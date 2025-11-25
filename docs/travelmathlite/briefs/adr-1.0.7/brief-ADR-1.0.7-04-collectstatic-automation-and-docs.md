# BRIEF: Automate collectstatic and operator docs

Goal

- Document and script the steps required to run `collectstatic` across local, CI, and deployment workflows so hashed assets are always present before WhiteNoise serves them (PRD §7 NF-004).

Scope (single PR)

- Files to touch: `scripts/` (add `scripts/run_collectstatic.py`), `docs/travelmathlite/ops/static-and-media.md`, `README.md` deployment section, checklist seeds referencing ADR-1.0.7.
- Tasks: create a reusable Python helper script (e.g., `scripts/run_collectstatic.py`) that can be invoked with `uv run python scripts/run_collectstatic.py` or executed directly; the script should call Django's management `collectstatic` in-process (via `django.core.management.call_command`) or by invoking `manage.py` with subprocess, accept flags (`--dry-run`, `--clear`), respect environment toggles (e.g., `USE_MANIFEST_STATIC=1` / `DJANGO_SETTINGS_MODULE`), capture stdout/stderr to log files, and optionally compress/archive logs for ADR evidence. Update documentation with a "Before deploy" checklist covering `STATIC_ROOT` cleanup, asset hashing verification, and artifact attachment expectations.
- Non-goals: Container builds, CDN upload automation, Windows batch parity (optional but nice to call out).

Standards

- Commits: `chore/docs` style; include Issue refs.
- Scripts should be implemented in Python 3.12, use a small CLI interface (prefer `argparse` / `click`), and be runnable via `uv run python scripts/run_collectstatic.py` or directly if executable. The script should prefer calling Django's `call_command('collectstatic', ...)` in-process when possible so it inherits the project's settings, and fall back to `subprocess` invocation when isolation is desired. Keep instructions reproducible and cross-platform.
- Tests: include at least one CI-friendly smoke test invoking the script with `--dry-run` or `--clear` flags to ensure it stays green. The CI job should set `DEBUG=False` and `USE_MANIFEST_STATIC=1` to produce a manifest artifact.

Acceptance

- A single documented command (e.g., `uv run python scripts/run_collectstatic.py`) runs `collectstatic` and stores output under `travelmathlite/staticfiles/` (or the configured `STATIC_ROOT`). The script accepts `--dry-run` and `--clear` flags and returns non-zero on failure.
- The script captures stdout/stderr to a timestamped log file under `docs/travelmathlite/ops/logs/` and produces a concise summary markdown (e.g., `docs/travelmathlite/ops/logs/collectstatic-summary-YYYYMMDD.md`) that records manifest presence, number of files copied, and any warnings.
- CHECKLIST seeds updated with a "Manifest storage enabled / WhiteNoise configured" verification box referencing this script. The ADR evidence folder should include the generated summary and (optionally) a zipped archive of raw logs.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Create `scripts/run_collectstatic.py` with a small CLI (argparse) that supports `--dry-run`, `--clear`, `--log-dir` and `--archive-logs`. Prefer `django.core.management.call_command('collectstatic', ...)` in-process so Django settings are loaded; if call_command is used, ensure `DJANGO_SETTINGS_MODULE` is set or accept a `--settings` override. The script should write detailed logs to `docs/travelmathlite/ops/logs/` and create a concise `collectstatic-summary-*.md` summarizing manifest presence, files copied, and exit status."
- "Update `docs/travelmathlite/ops/static-and-media.md` with a section describing how to run the new Python script locally and in CI, including required environment variables (`DEBUG=False`, `USE_MANIFEST_STATIC=1`) and an example CI job snippet that captures the summary as ADR evidence."
- "Add a README deployment snippet showing the `uv run python scripts/run_collectstatic.py --noinput` command in the release checklist and how to attach the generated summary and zip archive to the release artifacts."

---
ADR: adr-1.0.7-static-media-and-asset-pipeline.md
PRD: §7 NF-004
Requirements: NF-004
