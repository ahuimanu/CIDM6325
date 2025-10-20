# CIDM 6325 — Mini Tutorial: GitHub Copilot Instructions Files

A quick, practical guide for creating and using instructions so GitHub Copilot follows your project’s rules. This tutorial also covers personal custom instructions and path‑specific instructions. All examples use plain text (no emojis) and copy‑paste‑safe Markdown.

---

## 1) What is a Copilot instructions file?

A repository instructions file gives Copilot persistent, repository‑specific guidance: tech stack, build and test steps, coding conventions, and review rules. Copilot automatically attaches these instructions to Chat requests and certain GitHub surfaces when you work inside the repository.

File path (repository wide):
.github/copilot-instructions.md

---

## 2) Where to put instruction files and how they are used

* Repository wide: place a Markdown file at .github/copilot-instructions.md in the repository root. Supported clients will read it automatically when you open the repo.
* Path specific (advanced): create one or more .instructions.md files with an applyTo section to scope guidance to folders. Example under .github/instructions/.
* Personal custom instructions: configured at the user profile level on GitHub.com. Copilot will combine these with repository guidance when responding in the repo.

Tip: Add the repository instructions file early to reduce drift and standardize outputs.

---

## 3) What to put in the repository instructions file

Keep it concise and structured with headings and short bullet lists.

Suggested sections:

* Project overview
* Tech stack and versions
* Build and run commands
* Testing policy (mandatory rules)
* Coding standards and preferred patterns
* Security and secrets policy
* Pull request expectations
* Links to PRD, ADR index, contribution guide

Example section formatting:

``` markdown
# Project overview
- Domain, primary use cases, core modules.

# Tech stack and versions
- Python 3.12, Django 5.x, HTMX 1.9, Bootstrap 5.3.

# Build and run
- Setup: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
- Run: python manage.py migrate && python manage.py runserver
```

---

## 4) Do and Do Not

Do:

* State exact versions so Copilot suggests compatible APIs.
* Describe how to run and how to test locally.
* List naming conventions and module boundaries.
* Include anti‑goals that prevent churn.
* Update the file when standards change.

Do not:

* Paste long policies. Link to them instead.
* Include secrets or internal tokens.
* Use vague guidance. Prefer specific, testable norms.

---

## 5) Verifying the file is active

* In VS Code or Visual Studio, open a workspace that contains .github/copilot-instructions.md and ask Copilot Chat:
  What repository rules are you following?
  It should summarize sections from your file.
* If the IDE has a setting to enable repository instructions, turn it on and reload the window.

---

## 6) Governance companion files

Pair the repository instructions with:

* Pull request template: .github/pull_request_template.md
* Issue templates: .github/ISSUE_TEMPLATE/*.md
* CODEOWNERS for automatic reviewers
* ADR index under docs/adr/ with links from the instructions file

The PRD sets outcomes. The repository instructions tell Copilot how the team works so suggestions align with PRD, ADRs, and templates.

---

## 7) Prompt patterns that leverage instructions

A. Context probe
Read .github/copilot-instructions.md and summarize the rules you will follow for this repository. List any risks or ambiguities you see.

B. Task planning
Using our instructions file, propose a three‑commit plan to implement PRD section 2.3 (image uploads). Include file paths and acceptance checks.

C. PR help
Generate a PR description using our template, emphasizing test steps and a rollback plan. Call out any migrations or breaking changes.

---

## 8) Maintenance checklist

* Versions current and pinned (Python, Django, libraries)
* Build and test commands verified
* Policies reflect reality (naming, folders, review rules)
* Links valid (PRD, ADR, docs)
* Team agreed on anti‑goals

---

## 9) Example repository instructions file (drop‑in)

File:
.github/copilot-instructions.md

Body:

``` markdown
## Project overview
Django app for course assignments (CIDM 6325). Users submit projects; instructors review.

## Tech stack
Python 3.12 • Django 5.x • HTMX 1.9 • Bootstrap 5.3 • SQLite for development

## Build and run
- Setup: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
- Run: python manage.py migrate && python manage.py runserver

## Testing (MANDATORY)
- Test framework policy:
  - MUST use python -m unittest for pure Python modules.
  - MUST use Django’s built‑in test runner for Django apps: python manage.py test.
  - MUST NOT add or suggest pytest or any pytest plugins. If a proposal includes pytest, convert it to unittest or django.test.TestCase.
- Authoring tests:
  - Use unittest.TestCase or django.test.TestCase with clear, atomic cases.
  - Name files test_*.py and keep tests near the code under test.
- CI expectation: all tests must pass before merge.

## Coding standards
- PEP 8; type hints on new code; docstrings for public APIs.
- Views: prefer class‑based views for CRUD; function‑based views are acceptable for trivial endpoints.
- Forms: prefer ModelForm when mapping to models.

## Security
- No secrets in code; use environment variables. Follow the Django security checklist before deployment.

## Pull request expectations
- Small, atomic PRs (approximately 300 lines changed or less). Conventional commits (feat, fix, docs, refactor, test, chore).
- Fill the PR template with test steps and a rollback plan. Use squash merges.

## Links
- PRD: /docs/PRD.md
- ADR index: /docs/adr/README.md
- Contribution guide: /CONTRIBUTING.md
```

---

## 10) Custom instructions (personal, user‑level)

Personal custom instructions tailor Copilot Chat responses to your preferences across repositories. They complement repository instructions and do not replace them.

Where they live:

* On GitHub.com (profile level): Settings → Copilot → Custom instructions. You paste text into a form.
* Copilot does not read a file from your repo for personal instructions. To keep them versioned, maintain a local source file and paste its contents into the settings form when you update it.

Example local source file for students (copy‑paste body):
File to save in your repo for versioning only:
docs/copilot_personal_instructions.md

Body to paste into GitHub → Settings → Copilot → Custom instructions:

``` markdown
## Persona and tone
Be concise first, then provide brief rationale. Prefer numbered steps over prose.
Use Django 5.x norms.

## Testing policy (MANDATORY)

MUST use python -m unittest for pure Python modules.
MUST use Django’s built‑in test runner: python manage.py test.
MUST NOT suggest or use pytest or pytest plugins. Convert any pytest examples to unittest or django.test.TestCase.

## Coding preferences

Follow PEP 8; add type hints on new code; include docstrings for public APIs.
Prefer class‑based views for CRUD; function‑based views only for trivial endpoints.
Use ModelForm when mapping one‑to‑one to models.

## Pull request workflow

Propose atomic commits with Conventional Commit messages.
Always include a minimal diff, three risks, and three validation steps.
```

---

## 11) Instruction sources and precedence

When Copilot responds, it can combine multiple instruction sources:

1. Repository instructions (.github/copilot-instructions.md) for project rules.
2. Path‑specific instructions (.instructions.md with applyTo) scoped to folders or files in supported clients.
3. Personal custom instructions at your GitHub profile.

Guidance: keep project rules in the repository file, personal preferences in your profile, and special folder rules in path‑specific files.

---

## 12) Path‑specific instructions (advanced, optional)

Use path‑specific files when one area of the repository needs different rules (for example frontend versus backend).

``` markdown
File:
.github/instructions/frontend.instructions.md

Body:
applyTo:
- "frontend/**"
guidance:
- Use Bootstrap 5 utilities before adding custom CSS.
- Prefer progressive enhancement with HTMX; avoid SPA frameworks.
- Follow testing policy from .github/copilot-instructions.md (no pytest).

Note: Path‑specific support is available in VS Code Copilot Chat and Copilot coding agent flows.
```

---

## 13) Troubleshooting and validation

* Ask Copilot Chat: Which instructions are you following for this repository? It should reference both repository and, if enabled, your personal instructions.
* In VS Code: Chat → Configure → Instructions to view or edit active instruction files.
* In Visual Studio: enable loading of .github/copilot-instructions.md in Options → GitHub → Copilot → Custom instructions.

---

## 14) Quick patterns for personal custom instructions

A. Review‑first developer
Prefer small, atomic PRs. Always propose test stubs using Django TestCase. When suggesting changes, include a minimal diff and a rollback plan.

B. Educator mode
Explain solutions briefly first, then provide an annotated code block with three risks and three validation steps.

C. Safety and style
No secrets in code; environment variables only. Follow PEP 8; type hints on new code; docstrings for public APIs. Do not use pytest.

---

End of mini tutorial.
