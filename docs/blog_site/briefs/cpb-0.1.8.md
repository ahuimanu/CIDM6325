# BRIEF (cpb-0.1.8): Adopt uv/uvx and strict Ruff workflow

PRD Anchor

- docs/prd/blog_site_prd_v1.0.1.md §10 Acceptance (developer experience & code quality)

ADR Anchor

- ADR-0.1.0 (Django MVP)

Goal

- Standardize developer workflows with `uv` for environment and dependency tasks, `uvx` for tool execution, and `ruff` for lint + format, ensuring consistent, fast feedback.

Scope (single PR; ≤300 LOC)

- Document recommended `uv`-based workflows for Windows (bash) developers:
  - Create/activate venv (`uv venv .venv`)
  - Install dependencies (`uv pip install -r requirements.txt`)
  - Add packages (`uv pip install <pkg>` and update requirements if needed)
- Formalize `ruff` as both linter and formatter with a minimal, strict config:
  - Add `.ruff.toml` with rules, target-version, line-length, and isort import ordering
  - Document commands to check and fix locally (`uvx ruff format`, `uvx ruff check --fix`)
- Optional: pre-commit hook that runs ruff on staged files (document only in this slice).

Standards

- Python 3.12+; PEP 8; docstrings for public functions; type hints on new code.
- Conventional commits.
- No pytest introduction (Django TestCase remains the test framework).

Files to touch (anticipated)

- .ruff.toml (new)
- README.MD (update): quickstart with `uv` and `ruff` commands
- docs (new brief only, this file)

Proposed .ruff.toml (for implementation PR)

```toml
line-length = 100
indent-width = 4
target-version = "py312"

[format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[lint]
select = ["E", "F", "I", "N", "UP", "B", "C4"]
ignore = []

[lint.isort]
known-first-party = ["blog", "myblog"]
combine-as-imports = true
```

Acceptance

- `uv` is documented as the primary way to manage the local environment.
- `uvx ruff format` and `uvx ruff check` run cleanly on the repo after the PR that adds `.ruff.toml`.
- No changes to the Django testing approach (no pytest added).

How to Use (local)

```bash
# create venv and install
uv venv .venv
source .venv/Scripts/activate
uv pip install -r requirements.txt

# format and lint
uvx ruff format
uvx ruff check --fix
```

Prompts for Copilot

- "Add a .ruff.toml matching the proposed config; update README with uv/uvx usage."
- "Ensure ruff runs against the whole repo; add known-first-party modules."
- "Optional: generate a pre-commit config to run ruff on staged files."
