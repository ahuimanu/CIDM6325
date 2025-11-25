# copilot-instructions.md

Project norms

-   Language: Python 3.12 + Django.
-   Style: PEP 8; docstrings on public functions; type hints on new code.
-   Commits: Conventional (feat/fix/docs/refactor/test/chore). Include Issue references in commit messages using the keywords Refs (for ongoing work) and Closes (for the final commit when merging to the default branch).
-   Do not add pytest; use Django TestCase.

Tooling norms

-   Package and run with uv/uvx. Prefer `uv run` for Python entry points and `uvx` for ephemeral tools.
-   Lint and format with Ruff (use ruff for both lint and format; keep the repo lint-clean).
-   Keep commands reproducible in docs/scripts; avoid global pip installs.

Django norms

-   Views: prefer CBVs for CRUD; FBVs ok for trivial endpoints.
-   Forms: use ModelForm when mapping 1:1 to models.
-   Migrations: one logical change per migration.
-   Settings: read secrets from environment.

PR rules

-   Small PRs (<300 lines changed).
-   Include migration plan & rollback note.
-   Use Copilot PR summary to pre-brief reviewers.

UI testing and design

-   Use Playwright for UI flows, screenshots, and basic visual checks.
-   Store script(s) under `blog_site/scripts/` or app-equivalent; store screenshots under `blog_site/screenshots/` or feature-specific `docs/travelmathlite/screenshots/`.
-   Add at least one scripted flow per major feature (calculators, search, auth) that can run headless.

Wireframes

-   Derive low-fidelity wireframes from travelmath.com as references before building each feature.
-   Capture reference screenshots (Playwright or browser) and sketch wireframes (e.g., Excalidraw/Figma) targeting: distance calculator, nearest airport, cost estimator, search/results, and base layout.
-   Save artifacts under `docs/travelmathlite/wireframes/` with filenames `<feature>-wireframe-vX.*` and include brief notes on layout and interactions.

GitHub automations (ADRs, Briefs, FR/AC issues)

-   One ADR per PR. Create a dedicated branch per ADR (`adr/<id>-<slug>`) or use an issues‑only workflow on your base branch (e.g., `FALL2025`) if branch isolation isn't needed. Keep PRs small; include traceability (PRD §, FR/NF IDs). Title: `docs(adr): ADR-<id> <title>`.
-   **ALWAYS check available labels FIRST** before creating any GitHub Issue. Run `gh label list` to see what labels exist in the repository, then use only existing labels when creating issues.
-   For each Brief and each PRD Functional Requirement ID (e.g., `FR-F-001-1`) or Acceptance Criteria item, create a GitHub Issue using GitHub CLI. Include labels (e.g., `feature`, `FR`, `AC`, `travelmathlite`) and paste the acceptance notes.
-   Branches optional: if using per‑issue branches, link with `gh issue develop` and open PRs with `gh pr create` (enable Copilot PR summary). If using issues‑only, commit on the base branch and PR only when you open a feature branch. Always include the Issue reference in your commit messages (use Refs for ongoing work; Closes for the final commit merged to the default branch).

Copilot nudges (speak up)

-   When the user asks to commit or push, remind them to include the Issue reference in the commit message using the keywords "Refs" (ongoing) or "Closes" (final on merge). Example phrasing: include an Issue reference in the form Refs followed by the issue number, and mirror the same text as an Issue comment.
-   If a commit message draft lacks an Issue reference, propose an amended message that adds a Refs tag and show how to post the same text as an Issue comment.
-   If the user does not have the Issue number handy, ask for it or suggest a quick way to retrieve it (e.g., from the creation output or repository Issues list).
-   **Before creating any GitHub Issue**, always run `gh label list` first to check available labels, then use only existing labels in the issue creation command.
-   When generating GH CLI blocks that create Issues, always include `gh label list` as the first command before the issue creation command. Prefer patterns that print or export the Issue number so it can be reused for commit tagging and comments.
-   If the user indicates an issues‑only workflow, avoid suggesting per‑issue branches unless they explicitly request it; otherwise, confirm intent before proposing branches.

Commit + Issue comment sync

For each commit touching a brief/Issue, mirror the commit message as an Issue comment so they stay in sync (helps reviewers follow along):

-   Prepare your commit message (single line recommended for easy reuse).
-   Make the commit with that exact message.
-   Post the same text as an Issue comment to the related Issue (use its number).
-   Push your changes.

Example workflow: write the message once and reuse it for both the commit and the Issue comment. Keep the two messages identical. Use the keywords “Refs” for ongoing work and “Closes” for the final message merged to the default branch.
