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