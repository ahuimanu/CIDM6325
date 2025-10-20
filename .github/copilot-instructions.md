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