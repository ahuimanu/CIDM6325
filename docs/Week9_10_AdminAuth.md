# Weeks 9–10: Admin, Authentication, and File Uploads (Mapping to Rubric)

## Part A — Django Admin (30 pts)
- Enabled Admin (`/admin/`) and registered `Category`, `Tag`, `Post`, `Comment`.
- Customizations:
  - **PostAdmin**: `list_display`, `list_filter`, `search_fields`, `autocomplete_fields`, `ordering`, `fieldsets`.
  - **CommentAdmin**: compact list with `short_content` display.
- **Business use cases:**
  - Editors can search drafts by author/category and bulk publish.
  - Support staff can triage comments by post and date to moderate discussions.

## Part B — Authentication (30 pts)
- Implemented **registration** (UserCreationForm), login, logout.
- Role-based permission: `blog.can_publish` required to publish posts.
- **Security & usability notes:**
  - Password validators enabled; CSRF middleware on; HTTPS recommended in prod.
  - Autocomplete fields in admin reduce errors; clear validation messaging in forms.

## Part C — Peer Review (15 pts)
- Provide link/screenshot of comments on a peer’s repo. Evaluate admin discoverability, permission boundaries, and security posture.

## Part D — Blog Post (15 pts)
- See `docs/BlogPost_Productivity_vs_Security.md` (MD format, 500–700 words).

## Part E — Static & Uploaded Files (10 pts)
- Added `ImageField` to `Post`, updated forms/templates, `MEDIA_URL/MEDIA_ROOT` settings, and dev URL serving.

## Citations (Graduate Standard)
- Layman, *Understand Django*, Ch. 9 “Administer All The Things”, Ch. 11 “User Authentication”.
- Django 5.1 docs: https://docs.djangoproject.com/en/5.1/
- **AI Disclosure:** Prompts used for admin options and registration flow; outputs audited and revised for Django 5.
