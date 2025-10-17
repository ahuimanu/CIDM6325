# AI Transparency Log — Build a Blog (Feature Set 1 & 2)

##  Purpose
This document provides full disclosure of how AI tools  were used throughout the *Build a Blog* Django project.  
The log includes details of prompts, outputs, accepted/revised code, and reflection on AI’s role in the project.

---

## Project Context
**Course:** Web Application Development  
**Project:** Build a Blog (Feature Set 1 & 2)  


---

## 💬 AI Interaction Summary

| Date | Task | AI Assistance Description | Result | Human Action |
|------|------|----------------------------|---------|----------------|
| Oct 5, 2025 | Environment setup | Asked for guidance on creating and activating a virtual environment (`venv`) in VS Code | Clear step-by-step commands provided | Followed instructions, resolved PowerShell execution policy issue |
| Oct 5, 2025 | Django project creation | Requested help to create and start Django project (`startproject blog_project .`) | Command sequence and explanation provided | Project successfully started and verified at `http://127.0.0.1:8000` |
| Oct 5, 2025 | Debugging import error | Asked for fix after “No module named 'django'” error | AI explained that virtual environment was inactive | Activated `.venv` and installed Django |
| Oct 6, 2025 | Documentation support | Requested template for AI transparency and README | AI provided markdown templates following academic standards | Reviewing and updating content manually |
| Oct 7, 2025 | CRUD setup | Requested full code for views.py, forms.py, urls.py, and templates for CRUD blog posts | AI provided ready-to-use Django code with Bootstrap and HTMX integration | Code copied, tested, and adapted for project |
| Oct 7, 2025 | GitHub troubleshooting | Asked why push to org repo failed with 403 error | AI diagnosed GitHub permission issue and explained fix | 
| Oct 9, 2025 |	Configure App in settings.py | Consulted AI to verify correct way to register the posts app in INSTALLED_APPS. | Setup confirmed and migrations applied successfully. |	Added 'posts' to INSTALLED_APPS and verified database sync.|
| Oct 10, 2025 |	Create Blog Model (CRUD) |	Requested AI help to design Django model for blog posts (title, body, author, created_at, updated_at) with proper field types. |	Post model created in models.py with clear explanation of each field. |	Wrote model file using AI’s code and confirmed structure.|
| Oct 10, 2025 |	Database Migration |	Asked AI how to properly run makemigrations and migrate commands.	Database synced, Post model successfully added. |	Executed both commands in terminal and confirmed migration output.|
| Oct 11, 2025 |	Register Model in Admin	Used AI to generate code for registering Post model in admin.py with formatted display. |	Admin panel shows posts neatly with list_display enabled. |	Implemented AI’s @admin.register(Post) code and tested admin login.|
| Oct 11, 2025 |	Create Views and URLs |	Asked AI to create basic CRUD views (post_list, post_detail, post_create, post_update, post_delete) and URL routing. |	Views implemented, routes connected and tested without errors. |	Added code in views.py and urls.py; ran server to verify endpoints.|
| Oct 11, 2025 |	Templates Setup	Requested AI guidance to create templates/posts/ directory structure and link HTML files. |	Templates loaded correctly and integrated with views. |	Created templates folder, added HTML pages, and previewed in browser.|
---

## ⚙️ Prompts Used 

**Prompt 1:**  
> “Break it down step by step and explain to me how I will use VS Code and GitHub for submission.”

**Prompt 2:**  
> “I got the error ‘No module named django’. What should I do next?”

**Prompt Example 3:**  
> “Can you give me a full CRUD setup for my Django blog — views, forms, templates ”  

**Prompt Example 4:**  
> “Why am I getting a 403 error when I try to push to my professor’s GitHub repo?”
---

## 🧩 AI Outputs and Human Edits
- AI-generated setup commands and Django structure explanations were **accepted as instructional references**.  
- Code (such as `models.py`, `forms.py`, `views.py`, etc.) will be **reviewed and manually adapted** to meet project and accessibility requirements.  
- All explanations are **revised and verified** for understanding before implementation.

---

## 📖 Reflection Summary (Early Notes)
AI tools like ChatGPT have significantly accelerated the setup and debugging process.  
However, reliance on AI requires careful verification of:
- Correct syntax and context alignment with Django 5.2+
- Accessibility compliance (WCAG 2.2)
- Role-based permission logic and database relationships

---

**Last Updated:** October 11, 2025  
**Maintained by:** Demi Oluwafemi  
**Tool Used:** ChatGPT (GPT-5, OpenAI) , Co-Pilot 
