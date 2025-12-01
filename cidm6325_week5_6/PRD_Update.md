# PRD & Pitch Update

### Project Pitch
**AI Reflections Blog** is a learning journal that captures how students and professionals use AI during software development.  Each post documents a design decision—such as form validation, accessibility, or model architecture—and includes commentary on what AI suggested and how human reasoning refined it.  The goal is to make responsible AI adoption visible and analyzable in an academic setting.

---

## 1. User Roles
| Role | Permissions | Description |
|------|--------------|-------------|
| **Reader** | View published posts, search by keyword | Public audience exploring AI reflections |
| **Author** | Create, edit, and delete personal posts; comment on others | Authenticated contributors |
| **Editor** | Publish posts (permission `can_publish`), moderate comments | Faculty or reviewers with elevated rights |

---

## 2. Functional Requirements
- **Authentication:** Login/logout via Django’s built-in system.  
- **Forms & Validation:**  
  - `PostForm` validates title content and enforces a minimum body length of 50 characters.  
  - `CommentForm` screens for prohibited words.  
- **Multi-Model Design:**  
  - `Category → Post → Comment` (one-to-many)  
  - `Post ↔ Tag` (many-to-many)  
- **HTMX Search:** Dynamic filtering of posts without page reload.  
- **Accessibility (WCAG 2.2):**  
  Semantic labels, focus outlines, and ARIA roles for live alerts.

---

## 3. Non-Functional Requirements
- **Usability:** Responsive Bootstrap 5 layout with consistent navigation.  
- **Performance:** Whitenoise static serving and SQLite 3 backend.  
- **Maintainability:** Modular app structure (`blog/`, `config/`) and role-based permissions.  
- **Ethics & Privacy:** Data limited to voluntary posts; no personal analytics collected.

---

## 4. Data Model Overview
- **Category** – Groups related posts.  
- **Post** – Core reflection entry; linked to `User`, `Category`, and `Tag`.  
- **Tag** – Cross-categorical keywords for analytics.  
- **Comment** – Discussion layer referencing `Post`.  

*Relationships:*  
- `Category (1) – (M) Post`  
- `Post (M) – (M) Tag`  
- `Post (1) – (M) Comment`

---

## 5. Migration & Deployment Notes
- SQLite migrations created for new fields and relations.  
- Whitenoise middleware added for static assets.  
- GitHub Actions workflow (`.github/workflows/django.yml`) verifies build integrity on every commit.

---

## 6. Future Enhancements
- Inline HTMX editing and live comment updates.  
- Analytics dashboard showing tag frequency and author contribution trends.  
- Email notification system for post approval and publishing events.

---

## 7. Acceptance Criteria
- Validation errors appear inline under each form field.  
- Duplicate titles are rejected with clear user feedback.  
- Only Editors (users with `can_publish`) can toggle a post’s published state.  
- Application passes accessibility audit (keyboard navigation, focus visibility, color contrast).

---

### Summary
The Week 5–6 iteration transforms the blog from a simple CRUD project into a multi-model, accessibility-compliant learning artifact.  It now demonstrates how human-AI collaboration can produce maintainable, ethical, and educational software.
