
# BRIEF: Build blog post detail view slice

Goal

- Implement blog post detail view addressing individual post display functionality.

Scope (single PR)

- Files to touch: 
  - `blog/models.py` - Create Post model with required fields
  - `blog/views.py` - Create BlogPostDetailView
  - `blog/urls.py` - Add URL pattern for post detail
  - `templates/blog/blog_detail.html` - Create detail template
- Non-goals: 
  - Comments functionality
  - Social sharing buttons
  - Related posts sidebar

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).
- No secrets; env via settings.
- Django tests: use unittest/Django TestCase (no pytest).

Model Requirements

- Post model fields:
  - `title` - CharField(max_length=200) for blog post title
  - `author` - ForeignKey to User model for post author
  - `content` - TextField for main blog post content/body
  - `date_created` - DateTimeField(auto_now_add=True) for creation timestamp
  - `date_updated` - DateTimeField(auto_now=True) for last update timestamp
- Model methods:
  - `__str__()` method returning title
  - `get_absolute_url()` method for post detail URL
- Model Meta:
  - Default ordering by `-date_created` (newest first)

Acceptance

- User flow: User clicks on blog post title/link → navigates to `/blog/post/<id>/` → sees full post content with title, author, date, and body
- Post model supports all required fields for blog functionality
- Include migration? yes (model creation required)
- Update docs & PR checklist.

Prompts for Copilot

- "Create a Django Post model with title, author, content, date_created, and date_updated fields"
- "Generate a Django DetailView for blog posts with URL pattern `/blog/post/<int:pk>/`"
- "Create a blog post detail template with responsive design showing title, author, date, and content"
- "Add proper URL routing in blog/urls.py for the detail view"
- "Generate and run Django migrations for the Post model"
- "Explain changes and propose commit messages."
- "Generate unit tests for the Post model and blog post detail view functionality."