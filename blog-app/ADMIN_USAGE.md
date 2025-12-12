Admin Views: Business Use Cases and How to Use Them

This document explains the admin customizations implemented for the `blog` app and the business uses they support.

Files changed
- `blog/admin.py` — added admin customizations for `Post`, `Tag`, and `Comment` models. `PostAdmin` now includes list display columns, filters, a date hierarchy, a bulk `make_published` action, and an inline for comments. `TagAdmin` and `CommentAdmin` provide list displays, search, filters, and admin actions for moderation.

Business use cases

1) Editorial workflow and content publishing (PostAdmin)
- Goal: Allow editors to find posts that need attention, review them, and publish in bulk when ready.
- Admin features supporting this:
  - `list_filter` by `status` and `author` to quickly show drafts or posts in review.
  - `search_fields` on title and body to locate content by keywords.
  - `date_hierarchy` on `created_at` to browse recent activity by day/month.
  - `make_published` bulk action to publish multiple posts at once.
  - `CommentInline` so editors can view and moderate comments while viewing a post in the admin page.
- Expected users: Editors, content managers, course graders.

2) Comment moderation (CommentAdmin)
- Goal: Provide moderators a focused interface to review, approve/disapprove, and search comments.
- Admin features supporting this:
  - `list_filter` by `is_approved` and `created_at` to focus on unapproved or recent comments.
  - `search_fields` across comment body, post title, and commenter username to find problematic or high-value comments quickly.
  - `approve_comments` and `disapprove_comments` bulk actions to moderate multiple comments at once.
  - `list_select_related` to improve performance when displaying related `post` and `user` info.
- Expected users: Moderators, community managers.

3) Tag management and content analysis (TagAdmin)
- Goal: Manage tag vocabulary and quickly see how many posts use each tag for content planning.
- Admin features supporting this:
  - `list_display` of tag `name` and `post_count` to surface popular tags.
  - `search_fields` to find tags quickly.
- Expected users: Editors, analysts.

How to verify these admin features locally

1) Create or use an existing superuser:

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
# follow prompts to create admin user
```

2) Start the dev server:

```powershell
.venv\Scripts\python.exe manage.py runserver
```

3) Visit the admin site in your browser at http://127.0.0.1:8000/admin/ and log in with the superuser account.

4) Use the `Posts` admin list to filter by status, search by title, and try the `Mark selected posts as published` action.

5) Use the `Comments` admin to search and bulk-approve/disapprove comments. Open a Post in the admin to see its inline comments and moderate them there.

Notes and suggestions

- For production, consider adding audit logging for bulk actions (who published which posts) and a confirmation step for destructive actions.
- If comment volume grows, consider adding pagination, or a moderation queue with additional metadata (reason flags, reports count) to improve triage.

Contact
If you want any additional admin features (custom forms, export CSV actions, or integration with an external moderation tool), tell me which you'd like and I'll implement them and run the test suite.
