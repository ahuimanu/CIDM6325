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

### 4.2 Create an Issue from terminal

``` bash
gh issue create -t "Add <feature>" -b "PRD §<id>. Acceptance: …" -l enhancement
```

### 4.3 Start a dev branch linked to an Issue

``` bash
# Creates branch and links it to the issue; sets default base for PRs
gh issue develop <issue-number> --base main
git switch <auto-created-branch>
```

### 4.4 Make commits (small, atomic)

``` bash
git add -p
git commit -m "feat: add <feature> form and CBV\n\nPRD: §<id>; ADR: ADR-XXXX"
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

---

## 5) Vibe coding workflow (end‑to‑end)

1. **Pick a slice** from PRD → open/assign an **Issue** (well‑scoped).
2. Draft an **ADR** if you’re making a notable architectural choice.
3. Write a **Brief** (task‑level) and paste it into Copilot Chat.
4. **Implement in small steps**; ask Copilot to propose commits and diffs.
5. Open a **PR** with template + **Copilot PR summary**; request review.
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

* Scope fits one Issue; branch created via `gh issue develop`.
* Small, atomic commits with clear messages.
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
