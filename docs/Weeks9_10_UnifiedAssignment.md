# CIDM 6325 — Weeks 9–10 Unified Assignment
**Author:** Melodi Parton  
**Course:** CIDM 6325  
**Branch:** `feature/cbv-weeks-7-8`  
**Project:** Blog CRUD + Auth + Media Upload and Template Improvements  

---

##  Overview
This submission extends my Week 7–8 blog by completing Django authentication, adding a registration workflow, integrating image upload, and improving template usability.  
It also includes a peer review evaluating another student’s admin/auth implementation for usability, security, and business alignment.

---

##  Deliverables

### **Part A — Django Admin Implementation (30 points)**
- Implemented Django’s built-in authentication views under `/accounts/`.  
- Added a custom **user registration view** (`register`) and `register.html` template for new account creation.  
- Fixed logout behavior using a **GetLogoutView** to allow GET-safe logout and redirect to `/blog/`.  
- Updated `base.html` to include:  
  - `Blog | Login | Logout | Register` links  
  - Dynamic greeting: **“Hi {{ user.username }}”** when logged in.  
- Configured proper redirect paths in `settings.py`:
  ```python
  LOGIN_URL = "login"
  LOGIN_REDIRECT_URL = "blog:post_list"
  LOGOUT_REDIRECT_URL = "blog:post_list"

### **Part B — Authentication (30 points)**
- Protected create, update, and delete wiews with `LoginRequiredMixin.`
- Used `UserPassesTestMixin` to restrict editing/deleting to the post author.
- Auto-assigned `author = request.user` in `PostCreateView.`
- Updated templates to show **Edit | Delete** links only to the author.
- Verified unauthorized users cannot access restricted routes.

### **Part C - Peer Review (10pts)**
**Repository reviewed**: `boyhamgirl/CIDM6325_Week7_8 Unified`
I evaluated a peer’s admin/auth implementation focusing on:
- Usability: Clear login/logout flow and intuitive navigation consistent with Django conventions.
- Security: Proper use of LoginRequiredMixin, UserPassesTestMixin, and avoidance of GET-based destructive actions.
- Business Alignment: Auth workflow aligns with secure content management patterns for multi-user environments.
Feedback was posted in GitHub PR comments, commending clear role separation between usability, security, and business alignment.

### **Part D - Blog Post: Productivity vs Security (15 points)**
I wrote a 720 word Blog Post on on how Django Admin and Authentication support or hinder real business workflows.
- I made this an actual post in my Blog app.
- I also created this as an .md in my docs folder in my repository.

### **Part E - Enable Static Files and Uploaded Files (10 points)**
-Added an ImageField to Post Model in `blog/models.py`
-Installed and linked the Pillow library
-Configured media settings in `settings.py`
-updated your project-level `urls.py` 
-Updated `post_detail.html` to render the image
-Verified static files & media are both functional

### **AI Disclosure**
I used **ChatGPT (GPT-5)** and **GitHub Copilot** during development and documentation for this module.

**Accepted / Integrated Assistance:**
- Clarified Django configuration for `MEDIA_URL` and `MEDIA_ROOT` to enable uploaded image handling.
- Helped resolve the `Pillow` installation and verification process.
- Provided guidance for `ImageField` template rendering in `post_detail.html`.
- Drafted structured Markdown documentation for Parts A–E to match the course submission format.
- Assisted with proofreading and refinement of the “Productivity vs Security” blog post for clarity and flow.

**Rejected / Revised:**
- Automatically generated code snippets suggesting deprecated Django syntax (e.g., old `url()` patterns) were removed.
- Overly generic explanations were rewritten in my own words to align with project-specific implementation and course guidelines.

All code and text were reviewed, edited, and verified by me before inclusion in the final deliverable.  
My Django project was fully tested to confirm proper authentication, media upload behavior, and blog functionality.

---


  
  
  
  




