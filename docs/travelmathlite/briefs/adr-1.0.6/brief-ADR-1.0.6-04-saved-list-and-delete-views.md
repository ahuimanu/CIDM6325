# BRIEF: List and delete saved calculations (per-user)

Goal

- Build views and templates for authenticated users to list and delete their saved calculations, capped at 10 items, private by default (PRD §4 F-006; NF-003).

Scope (single PR)

- Files to touch: `apps/trips/views.py` (CBVs: `SavedCalculationListView`, `SavedCalculationDeleteView`), `apps/trips/urls.py`, templates `apps/trips/templates/trips/saved_list.html`, `.../saved_confirm_delete.html`.
- Behavior: Per-user queryset filtering; pagination optional; delete confirmation view; link from user menu/nav; no cross-user access.
- Non-goals: Editing saved rows; sharing/exporting.

Standards

- Commits: conventional (feat/docs); include Issue reference.
- CBVs preferred; enforce `LoginRequiredMixin` and object-level filtering by `request.user`.

Acceptance

- Authenticated users can reach a "Saved Calculations" page listing up to 10 items with newest first.
- Users can delete their own items; others' items are not accessible (404/403).
- Templates extend base and show calculator type, created date, and optional preview of inputs/outputs.
- Include migration? no
- Update docs & PR checklist.

Prompts for Copilot

- "Implement `SavedCalculationListView` and `SavedCalculationDeleteView` using `LoginRequiredMixin` and per-user filtering in `get_queryset()`."
- "Create templates `saved_list.html` and `saved_confirm_delete.html` with a simple table/list and delete button per row; add URL routes under `apps/trips/urls.py`."
- "Add nav link to saved list visible only for authenticated users."

---
ADR: adr-1.0.6-auth-and-saved-calculations-model.md
PRD: §4 F-006; §7 NF-003
Requirements: FR-F-006-1, NF-003; Invariants: INV-1, INV-2
