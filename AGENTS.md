# CIDM 6325 — GitHub Copilot “Vibe Coding” Playbook

*A practical guide for students who already have a PRD. This doc shows how your PRD connects to working artifacts (ADRs, Briefs, instruction files), and how to use GitHub Copilot + GitHub CLI to ship clean PRs and Issues.*

---

## 0) Why this doc

* **You already wrote a PRD.** Now you’ll *work the plan* with light governance that doesn’t slow you down.
* **Vibe coding ≠ random coding.** Use Copilot as your co‑driver: keep prompts scoped, context rich, and outputs reviewable. Focus on: context windows, task scoping, repository instructions, issue‑first workflows, PR summaries.

---

## 1) Artifact relationships: PRD → ADRs → Briefs → Code/PRs

* **PRD (Product Requirements Doc)**: “What & why” at feature level. Stable for the sprint.
* **ADR (Architecture Decision Record)**: One decision per record (driver, options, trade‑offs, decision, consequences). Keep these short; link back to the PRD section that motivated the decision.
* **Briefs (Copilot‑facing prompts)**: Task‑level instructions that translate PRD/ADR intent into *actionable* steps for Copilot.
* **Instruction files** (repo‑level guardrails): `copilot-instructions.md`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/…`, `CODEOWNERS`. These give Copilot and contributors the rules of the road.

> Rule of thumb
> **PRD** = outcomes; **ADR** = irreversible choices; **Brief** = how we’ll do the next slice; **Instruction files** = house rules.

---

## 2) Copilot best practices (distilled)

1. **Provide helpful context**
   Keep the right files open; close irrelevant ones. Start a new chat if context drifted.
2. **Scope the task**
   Well‑scoped issues work best; pick tasks that are small and reviewable.
3. **Iterate in comments/PRs**
   Ask Copilot to refine code in response to review comments; use it to draft/update PR descriptions.
4. **Leverage repository instructions**
   Put conventions in `copilot-instructions.md` so Copilot adheres to them.
5. **Use Chat commands wisely**
   Keep a cheat‑sheet of useful editor commands and quick prompts.
6. **PR summaries**
   Use Copilot to generate a PR summary that highlights files and reviewer focus areas (works best starting from a blank description).

7. **Tooling defaults (class policy)**
   * Use `uv run` / `uvx` to execute Python entry points and ephemeral tools.
   * Lint and format with Ruff (keep the repo lint-clean).
   * Use Playwright for UI flows and visual checks; keep scripts under `blog_site/scripts/` or app-equivalent; store screenshots under `blog_site/screenshots/` or `docs/travelmathlite/screenshots/`.
   * Create low-fidelity wireframes from travelmath.com before each feature; save in `docs/travelmathlite/wireframes/`.

---

## 3) Minimal templates (copy & adapt)

### 3.1 ADR (lightweight)

``` markdown
# ADR-XXXX: <Concise Decision>
Date: YYYY-MM-DD
Status: Proposed | Accepted | Superseded by ADR-YYYY

Context
- PRD link: <#section-or-issue>
- Problem/forces

Options
- A) ...
- B) ...

Decision
- We choose <A/B> because ...

Consequences
- Positive: …
- Negative/Risks: …

Validation
- Measure/rollback: …
```

### 3.2 Copilot Brief (task‑level; for “vibe coding” guidance)

``` markdown
# BRIEF: Build <feature> slice

Goal
- Implement <feature> addressing PRD §<id>.

Scope (single PR)
- Files to touch: …
- Non-goals: …

Standards
- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Acceptance
- User flow: …
- Include migration? yes/no
- Update docs & PR checklist.

Prompts for Copilot
- "Generate a Django Form + view for … with success redirect to …"
- "Explain changes and propose commit messages."
- "Refactor into CBV while preserving behavior; show diff-ready patch."
```

### 3.3 `copilot-instructions.md` (repo rules Copilot should follow)

``` markdown
# copilot-instructions.md

Project norms
- Language: Python 3.12 + Django.
- Style: PEP 8; docstrings on public functions; type hints on new code.
- Commits: Conventional (feat/fix/docs/refactor/test/chore).
- Do not add pytest; use Django TestCase.

Django norms
- Views: prefer CBVs for CRUD; FBVs ok for trivial endpoints.
- Forms: use ModelForm when mapping 1:1 to models.
- Migrations: one logical change per migration.
- Settings: read secrets from environment.

PR rules
- Small PRs (<300 lines changed).
- Include migration plan & rollback note.
- Use Copilot PR summary to pre-brief reviewers.
```

### 3.4 PR & Issue templates

``` markdown
# .github/pull_request_template.md

## Summary
Problem & why now.

## Changes
- …

## How to Test
1) …
2) …

## Risks/Rollback
- Risk: Low/Med/High
- Rollback: `git revert <merge-commit>`

## Links
PRD §<id>, ADR-XXXX, Issue #<id>

# .github/ISSUE_TEMPLATE/feature_request.md

name: Feature request
body:
- type: textarea
  attributes:
    label: Outcome
    description: Link PRD section and describe the user-visible win.
- type: textarea
  attributes:
    label: Acceptance criteria
- type: textarea
  attributes:
    label: Implementation hints / Copilot prompts
```

---

## 4) GitHub CLI: create Issues & PRs fast (and clean)

### 4.1 Setup

``` bash
gh auth login
gh repo clone <org>/<repo> && cd <repo>
```

### 4.2 Create an Issue from terminal and capture the number

``` bash
# FIRST: Check available labels in the repo
gh label list

# Create Issue and capture the number for commits
# Note: gh CLI's -q flag works without jq (built-in JSON query)
ISSUE_NUM=$(gh issue create \
  -t "Add <feature>" \
  -b "PRD §<id>. Acceptance: …" \
  -l enhancement \
  --json number -q '.number')

echo "Created Issue #${ISSUE_NUM}"
```

**Windows Git Bash alternative (if -q doesn't work):**

``` bash
# FIRST: Check available labels
gh label list

# Git Bash: capture URL and extract number with sed/regex
ISSUE_URL=$(gh issue create \
  -t "Add <feature>" \
  -b "PRD §<id>. Acceptance: …" \
  -l enhancement)
ISSUE_NUM=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_NUM}"
```

**Windows PowerShell alternative:**

``` powershell
# FIRST: Check available labels
gh label list

# PowerShell: capture output and parse manually
$ISSUE_URL = gh issue create -t "Add <feature>" -b "PRD §<id>. Acceptance: …" -l enhancement
$ISSUE_NUM = $ISSUE_URL -replace '.*?(\d+)$', '$1'
Write-Host "Created Issue #$ISSUE_NUM"
```

**Complete workflow (Git Bash one-liner):**

``` bash
# Create Issue, commit, comment, and push in one sequence
ISSUE_URL=$(gh issue create -t "Title" -b "Body") && \
ISSUE_NUM=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#') && \
echo "Created Issue #${ISSUE_NUM}" && \
COMMIT_MSG="prefix: description — Refs #${ISSUE_NUM}" && \
git add -A && \
git commit -m "$COMMIT_MSG" && \
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG" && \
git push && \
echo "✓ Done! Issue #${ISSUE_NUM}"
```

### 4.3 Start work from an Issue

``` bash
# Option A (issues-only, no branch): stay on your base (e.g., main/FALL2025)
# - Create the Issue with `gh issue create ...` and commit directly on the base branch
# - Use PRs later only if you create a feature branch

# Option B (branch per Issue): create & link a branch to the Issue
gh issue develop <issue-number> --base main
git switch <auto-created-branch>
```

### 4.4 Make commits (small, atomic)

``` bash
# Using the captured ISSUE_NUM from 4.2
COMMIT_MSG="feat: add <feature> form and CBV — Refs #${ISSUE_NUM}

PRD: §<id>; ADR: ADR-XXXX"

git add -A
git commit -m "$COMMIT_MSG"

# Post the same message as an Issue comment so they stay in sync
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"

git push

# Optional (final): when you intend to close the Issue on merge to default
# COMMIT_MSG="feat: complete <feature> — closes #${ISSUE_NUM}"
# git commit -m "$COMMIT_MSG" && gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG" && git push
```

### 4.5 Open a PR from your branch

``` bash
gh pr create --fill --title "feat: <feature>" --body-file .github/pull_request_template.md
gh pr view --web   # open it in browser
```

### 4.6 Ask Copilot for a PR summary

* On the PR page, use **Copilot PR summary** to generate a prose overview and focus list for reviewers (works best with an empty description to start).

### 4.7 Merge policy (recommended for class)

``` bash
gh pr merge --squash --delete-branch
```

### 4.8 ADR and Issue automation (policy)

``` bash
# FIRST: Always check available labels before creating issues
gh label list

# ADRs: one ADR per PR
gh issue create -t "docs(adr): ADR-<id> <title>" -b "Link PRD sections and FR/NF IDs. Keep PR small." -l docs,adr,travelmathlite
# Issues-only workflow: commit on base branch; if you prefer, create a branch per Issue:
# gh issue develop <issue-number> --base main && git switch <auto-created-branch>
# commit changes for ADR files...
gh pr create --title "docs(adr): ADR-<id> <title>" --body "Traceability: PRD §<id>, FR-*, NF-*; see ADR." --fill

# FR/AC items: create Issues per PRD FR-F-###-N or Acceptance Criteria
gh issue create -t "FR-F-001-1: <short>" -b "Acceptance: …\nTrace: PRD §4 F-001" -l feature,FR,travelmathlite
gh issue create -t "AC: <feature> - <short>" -b "Acceptance: …\nTrace: PRD §<id>" -l AC,feature,travelmathlite
```

---

## 5) Vibe coding workflow (end‑to‑end)

1. **Pick a slice** from PRD → open/assign an **Issue** (well‑scoped).
2. Draft an **ADR** if you’re making a notable architectural choice. Open a dedicated PR for each ADR (branch `adr/<id>-<slug>`; title `docs(adr): ADR-<id> <title>`), and link PRD sections and FR/NF IDs.
3. Write a **Brief** (task‑level) and paste it into Copilot Chat.
4. **Implement in small steps**; ask Copilot to propose commits and diffs.
5. Open a **PR** with template + **Copilot PR summary**; request review. For FR/AC work items, create an Issue per PRD `FR-F-###-N` or AC line. Workflow: issues-only (stay on base) or branch-per-issue (link with `gh issue develop`).
6. Iterate using **comments**; ask Copilot to address reviewer feedback.
7. **Squash merge**; link PR to Issue and ADR; update the PRD if the slice changes scope.

---

## 6) Prompt patterns that work well (paste into Copilot Chat)

**A. Code‑gen (scoped)**
Context: Working on PRD §2.1 “User file uploads”.
Task: Create a Django CBV + ModelForm for Image upload with size/type validation,
success redirect to detail page, and template snippet.
Constraints: PEP 8, type hints on new code, no pytest (use Django TestCase stubs).
Deliverables: Proposed file changes and 2-3 atomic commit messages.

**B. Refactor (safety‑first)**
Task: Convert function-based view upload() to a CBV with identical behavior.
Keep URLs stable. Include tests using Django TestCase. Show a minimal diff and
call out risks and a rollback plan.

**C. PR polish**
Task: Generate a concise PR summary for reviewer focus. List impacted files
and any migrations. Include “How to Test” steps and risk/rollback notes.

---

## 7) Quality checklist (use before opening a PR)

* Scope fits one Issue; branch optional (issues-only on base branch is acceptable).
* Small, atomic commits with clear messages.
* Commits reference the Issue (Refs #ISSUE_NUM for ongoing; closes #ISSUE_NUM for final when merging to default).
* Commit message and the Issue comment remain identical for each change to keep discussion and history aligned.
* No secrets; settings via environment.
* Docs and templates updated (`copilot-instructions.md`, PR template).
* Ask Copilot for a **PR summary**; sanity‑check it.

---

## 8) Quick reference (handy pointers)

* Copilot: best practices for context, scoping, resetting chats.
* Copilot Chat: prompting patterns and commands.
* Working on tasks: well‑scoped issues, repo instructions, iterate via comments.
* PR summaries: how to auto‑summarize changes.
* GitHub CLI: `gh pr …`, `gh issue …`.

---

### Appendix: Why “vibe coding” still needs receipts

* **Receipts beat vibes.** The vibe gets you moving; ADR + Brief + Issue + PR give you *receipts* for what changed and why.
* **Copilot amplifies whatever you feed it.** Strong inputs (PRD anchors, repo instructions, scoped issues) → strong outputs. Weak inputs → weak outputs.

*End of document.*
