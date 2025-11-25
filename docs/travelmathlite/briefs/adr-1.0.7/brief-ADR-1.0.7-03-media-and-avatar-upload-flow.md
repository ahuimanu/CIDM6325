# BRIEF: Implement local media handling and avatar upload flow

Goal

- Provide a simple avatar upload path stored under `MEDIA_ROOT/avatars/`, guarded by an env flag so the feature can be enabled for local demos without requiring third-party storage (PRD §4 F-007; §7 NF-004).

Scope (single PR)

- Files to touch: `travelmathlite/core/settings.py` (env flag, media defaults), `apps/accounts/models.py` (new `Profile` w/ optional `avatar` `ImageField`), `apps/accounts/forms.py` or `views.py` (profile form/view), `apps/accounts/templates/accounts/profile_form.html`, url wiring, and `docs/travelmathlite/ops/static-and-media.md` for operator instructions.
- Tasks: add `ALLOW_AVATAR_UPLOADS` env toggle; create profile editing view restricting uploads to authenticated users; ensure uploaded files land in `MEDIA_ROOT/avatars/` and are served via `MEDIA_URL` in dev; add sample placeholder image when avatar absent.
- Non-goals: Remote storage (S3, CDN), drag-and-drop cropping, avatar listing APIs.

Standards

- Commits: conventional; include Issue refs.
- Update dependencies with `Pillow` to support `ImageField`; run `uv pip compile`/`uv sync` as needed.
- Tests implemented with `django.test.TestCase`, using temporary media override via `override_settings(MEDIA_ROOT=tmpdir)` to avoid polluting repo.

Acceptance

- Authenticated user can visit `/accounts/profile/` (or similar) to upload an avatar when `ALLOW_AVATAR_UPLOADS=true`; feature hidden otherwise.
- Uploaded files stored under `<repo>/travelmathlite/media/avatars/` with unique filenames and validated content type/size (reject >1MB or non-image input).
- Templates display avatars via `{% if user.profile.avatar %}` using `MEDIA_URL`; fallback placeholder is pulled from static assets.
- Include migration? yes (Profile model + ImageField)
- Update docs & PR checklist.

Prompts for Copilot

- "Create an `accounts.Profile` model linked via `OneToOneField` to `User` with an optional `ImageField(upload_to='avatars/')` and signals to auto-create/maintain the profile."
- "Add a `ProfileUpdateView` (CBV) that uses `LoginRequiredMixin` and `ModelForm` to handle avatar upload/delete toggles, gating view availability by an `ALLOW_AVATAR_UPLOADS` setting."
- "Write tests that override `MEDIA_ROOT` with `tempfile.mkdtemp()` to verify avatar files are saved and cleaned up."

---
ADR: adr-1.0.7-static-media-and-asset-pipeline.md
PRD: §4 F-007; §7 NF-004
Requirements: FR-F-007-1, NF-004
