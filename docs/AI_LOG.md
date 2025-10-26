# 🤖 AI Tooling Lab Log — Smart Scheduler (CIDM 6325)

**Author:** Melodi Parton  
**Course:** CIDM 6325 – Web App Development with Django  
**Instructor:** Dr. Jeffry Babb  
**Semester:** Fall 2025  

---

## 🧠 Purpose

This document records how AI tools were used throughout the development of the **Smart Scheduler** project and the **Django Blog (Module 4)** feature.  
It provides a transparent log of AI-assisted coding, design support, and learning interactions aligned with West Texas A&M University’s ethical use guidelines.

---

## 🧰 Tools Used

| Tool | Purpose | Use Case |
|------|----------|----------|
| **ChatGPT (GPT-5)** | Code generation, error troubleshooting, README and documentation support | Debugging, testing, writing view logic, and editing Markdown deliverables |
| **GitHub Copilot** | Inline code suggestions and auto-completions | Django CBVs, URL patterns, form/model logic |
| **VS Code** | Development environment with Copilot integration | Code editing, running Django server, managing venv |
| **GitHub** | Version control and collaboration | Branch creation, commits, pull requests |
| **Django Admin** | Validation and CRUD verification | Created and tested posts, users, and admin access |
| **Docker** | Local database containerization | PostgreSQL setup and testing environment |

---

## 🧩 Major Tasks Assisted by AI

### 1️⃣ Django Setup and Structure
- Created `pyproject.toml` to declare Django 5.2.6 as the dependency.  
- AI provided exact configuration for `settings.py`, app registration, and URL routing (`core/urls.py` and `blog/urls.py`).  
- Debugged import errors (e.g., missing `PostList` attribute).

### 2️⃣ Class-Based Views (CBVs)
- ChatGPT generated initial templates for `PostList`, `PostDetail`, `PostCreate`, `PostUpdate`, and `PostDelete` using **LoginRequiredMixin** and **UserPassesTestMixin**.  
- Copilot suggested completion logic for `form_valid()` methods and slug handling.  
- Verified permissions so that only authors could edit or delete posts.

### 3️⃣ Templates and Slugs
- AI explained how to use `{% url 'blog:post_detail' slug=post.slug %}` and helped correct path matching errors.  
- Built templates (`post_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`) with Bootstrap styling.  
- Implemented `slugify()` to generate unique slugs from post titles.

### 4️⃣ Authentication & User Management
- Added login/logout views using Django’s built-in auth system.  
- AI guided the separation between **admin users** and **normal authors**, ensuring proper permission checks (`is_staff`, `is_superuser`).

### 5️⃣ README & Documentation Support
- ChatGPT helped write structured sections for:
  - `README.md` — including **Deliverables**, **Test URLs**, and **Artifact Summary Table**
  - `AI_LOG.md` — to meet reflection and ethical disclosure requirements  
- Ensured Markdown was standards-compliant with headings, tables, and links.

### 6️⃣ Testing and Debugging
- Resolved AttributeError: `module 'blog.views' has no attribute 'PostList'`.  
- Corrected view imports, indentation, and file placement issues.  
- Verified URLs using test paths (e.g., `/blog/new/`, `/blog/<slug>/edit/`, `/accounts/login/`).

---

## 💬 Reflection on AI Use

| Aspect | Reflection |
|--------|-------------|
| **Effectiveness** | AI accelerated troubleshooting and clarified Django’s architecture. It helped interpret stack traces and provided structured code corrections. |
| **Learning Value** | Enhanced understanding of CBVs, mixins, and URL routing. Reinforced knowledge of authentication flow and template inheritance. |
| **Limitations** | AI occasionally proposed outdated Django syntax or omitted imports. Manual verification with the Django 5.2.6 documentation was necessary. |
| **Human Oversight** | Final code review, testing, and logic validation were done manually in VS Code to ensure correctness and ethical compliance. |

---

## ⚖️ Ethical Considerations

AI assistance was used **transparently** and within course policy.  
- All generated code was **reviewed, tested, and understood** before inclusion.  
- No uncredited or unverified code was submitted as original work.  
- The AI’s role was advisory and educational — not a substitute for independent coding effort.  
- This log serves as full disclosure of AI involvement per WTAMU academic integrity standards.

---

## 🧾 Summary

| Category | Description |
|-----------|--------------|
| **Project** | Smart Scheduler + Django Blog (Module 4) |
| **Main Focus** | CRUD, Authentication, and Slug-based routing |
| **AI Contribution** | Guidance, troubleshooting, documentation |
| **Human Contribution** | Code validation, testing, ethical reflection |
| **Outcome** | Functional blog with secure author permissions and professional documentation |

---

### 📎 References
- [Matt Layman — *Understand Django*](https://www.mattlayman.com/understand-django/)  
- [Django Documentation](https://docs.djangoproject.com/en/5.2/)  
- [WTAMU CIDM 6325 Course Resources]  
- [Bootstrap 5 Framework](https://getbootstrap.com/)  

---

*Prepared by Melodi Parton — CIDM 6325 Fall 2025 — AI Lab Log Submission*

---

## 2025-10-12 — Week 5–6 Blog Refactor and CBV Implementation  

**Context:**  
Refactored the Blog application to use Django Class-Based Views (CBVs) and  
implemented full CRUD functionality with authentication, permissions, and  
form validation. Updated templates for Create, Update, Delete, and Detail  
views, ensuring DRY (Don’t Repeat Yourself) principles and clean inheritance  
via `LoginRequiredMixin` and `UserPassesTestMixin`.  

**AI Assistance:**  
ChatGPT (GPT-5) provided  guidance in refactoring from FBVs to CBVs,  
debugging mixin logic, improving template inheritance, and confirming proper  
URL/view connections. It also assisted with PR documentation (`Week7_8_CBVs.md`)  
and verifying repo branch merges.  

**Outcome:**  
Completed the CBV refactor successfully, verified CRUD functionality, and  
prepared the project for modular design and scalability analysis in upcoming  
weeks.

---

## 2025-10-25 — Week 7–8 Architecture Critique Added  

**Context:**  
Finalized Part B deliverable (*Architecture Critique*) and documented it in  
`/docs/week_7_8_architecture_critique.md` as part of the Weeks 7–8 submission.  

**AI Assistance:**  
ChatGPT (GPT-5) guided the process of structuring and formatting the Markdown  
document, ensuring APA-style organization and rubric alignment. It also  
assisted with Git commands to commit and push the file to the  
`feature/cbv-weeks-7-8` branch and verified the pull-request merge readiness.  

**Outcome:**  
Successfully added the Architecture Critique to `/docs`, updated the branch,  
and confirmed that the pull request is ready for instructor review.
