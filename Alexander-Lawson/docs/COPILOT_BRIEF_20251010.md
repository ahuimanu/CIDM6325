# BRIEF: Build Blog View Page Slice

Goal

- Implement a blog view page addressing PRD §1.2.

Scope (single PR)

- Files to touch:  
  - `myblog/models.py`  
  - `myblog/views.py`  
  - `myblog/urls.py`  
  - `myblog/templates/myblog/blog_list.html`  

- Non-goals:  
  - Advanced styling or JavaScript functionality.  
  - Pagination or filtering of blog posts.  

Standards

- Commits: conventional style (feat/fix/docs/refactor/chore).  
- No secrets; env via settings.  
- Django tests: use `unittest`/`Django TestCase` (no pytest).  

Acceptance

- User flow:  
  - A user navigates to `/blog/` and sees a list of blog posts with titles, publication dates, and content previews.  
  - Clicking on a post redirects to a detailed view (not implemented in this task).  

- Include migration? yes  
- Update docs & PR checklist.  

Model

- **Name:** `BlogPost`  
- **Fields:**  
  - `title` (CharField, max_length=200)  
  - `content` (TextField)  
  - `published_date` (DateTimeField)  
  - `author` (ForeignKey to `auth.User`, on_delete=models.CASCADE)  

Prompts for Copilot

- "Generate a Django model for a blog post with fields for title, content, published date, and author."  
- "Generate a Django view, URL, and template for a blog list page with success redirect to `/blog/`."  
- "Explain changes and propose commit messages."  
- "Refactor into CBV while preserving behavior; show diff-ready patch."