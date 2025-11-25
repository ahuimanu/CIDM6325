# Copilot Brief: ADR-1.0.0-04 Templates Organization by App

## Goal
Organize templates under per-app directories and verify includes resolve without conflicts.

## Scope
- For each app, create `templates/<app>/` and add a minimal `index.html` and partials as needed.
- Adopt standard include paths to avoid collisions.
- Non-goals: full base layout.

## Standards
- Lint and format with Ruff; conventional commits.
- Autoescape remains enabled.

## Acceptance
- Each app renders its `index.html` with `{% extends 'base.html' %}` or app base; includes resolve.
- No template name collisions across apps.

## Prompts for Copilot
- Create per-app templates with minimal content and an include to demonstrate resolution.
- Show how to name partials to prevent collisions and update includes accordingly.

---
ADR: ADR-1.0.0
PRD: §4 Scope (F-007), §13 Traceability
