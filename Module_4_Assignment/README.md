# Module 4 – CIDM 6325: Class-Based Views + Application Architecture

**Author:** Mafruha Chowdhury  
**Course:** CIDM 6325 – Electronic Commerce (Fall 2025)  
**Focus:** Refactoring CRUD features with Class-Based Views (CBVs), analyzing Django modular architecture, and critiquing instructor exemplars.

---

##  Table of Contents
1. [Overview](#overview)
2. [Part A – CBV Implementation](#part-a--cbv-implementation)
3. [Part B – Application Architecture Critique](#part-b--application-architecture-critique)
4. [Part C – Peer Review](#part-c--peer-review)
5. [Part D – Discussion Summary](#part-d--discussion-summary)
6. [Part E – TravelMathLite Critique](#part-e--travelmathlite-critique)
7. [AI Use Disclosure](#ai-use-disclosure)
8. [References](#references)

---

##  Overview
This module builds on the logistics delivery app from **Module 3**, transitioning from Function-Based Views (FBVs) to **Class-Based Views (CBVs)** to improve scalability, maintainability, and modular design.

The goals are to:
- Refactor CRUD functionality using Django’s `ListView`, `CreateView`, and `UpdateView`.
- Demonstrate inheritance, mixins, and modular reuse.
- Critique Django’s architecture (app structure & CBVs).
- Provide peer review and discuss scalability.
- Evaluate instructor’s **TravelMathLite** exemplar.

---

##  Part A – CBV Implementation

###  Objective
Refactored all CRUD features from Module 3 using Class-Based Views, including create, read, update, and delete operations.

###  Implementation Summary
- **App:** `logistics_app`
- **Model:** `Order` (related to `Customer`)
- Added `Customer` creation view and template (`create_customer.html`)
- URL: `/customer/create/`
- **Refactored Views:**  
- `OrderListView` → extends `ListView`  
- `OrderCreateView` → extends `CreateView` + `SuccessMessageMixin`  
- `OrderUpdateView` → extends `UpdateView` + `SuccessMessageMixin`  
- `OrderDeleteView` → extends `DeleteView` + `SuccessMessageMixin`  
- **Templates:** `order_list.html`, `order_form.html`, `order_confirm_delete.html`, `index.html`, `base.html`, `logged_out.html`, `registration/login.html`

- **Mixins Used:** `LoginRequiredMixin`, `SuccessMessageMixin`
---
- **Authentication:**
- Implemented login/logout using Django’s authentication system
- `LoginRequiredMixin` enforces access control for all CRUD views
- Templates added: `registration/login.html`, `logged_out.html`


###  FBV vs CBV Trade-Off Analysis
| Criteria | Function-Based Views (FBVs) | Class-Based Views (CBVs) |
|-----------|-----------------------------|---------------------------|
| **Readability** | Simple and explicit logic | Compact but requires familiarity |
| **Reusability** | Limited – must duplicate logic | High – inheritance and mixins |
| **Extensibility** | Manual decorators | Built-in inheritance system |
| **Learning Curve** | Lower | Moderate – conceptual abstraction |
| **Use Case** | Quick prototypes | Scalable modular apps |

---

- **Navbar Enhancement**
- Dynamic navbar includes conditional display of “Login” / “Logout” and highlights active routes.
- Admin portal now includes link back to root app view.

**Conclusion:**  
CBVs abstract repetitive CRUD operations, enabling modular, scalable design while maintaining Django’s “Don’t Repeat Yourself” philosophy.

---

##  Part B – Application Architecture Critique
A 2–3 page critique (see [`docs/PartB_Critique.docx`](docs/PartB_Critique.docx)) analyzes Django’s app architecture:
- Strengths of modular apps and reusability
- Role of CBVs in promoting maintainability
- Limitations and design trade-offs
- Opportunities for layered extension in enterprise projects

---

##  Part C – Peer Review
Peer review performed on another student’s CBV implementation:  
- Evaluated clarity and modularity  
- Left GitHub comments on naming and inheritance patterns  
- Submitted review summary in [`docs/PEER_REVIEW.md`](docs/PEER_REVIEW.md)

---

##  Part D – Discussion Summary
The discussion post (~500 words) focuses on:
- Django’s CBV architecture and modularity  
- How app-based organization scales enterprise apps  
- Peer responses (≥150 words each) summarized in [`docs/PARTE.md`](docs/PARTE.md)

---

##  Part E – TravelMathLite Critique
Evaluation of the instructor’s **TravelMathLite** example (combined Modules 3 & 4 assignment).  
See [`docs/PartE_TravelMathLite.md`](docs/PartE_TravelMathLite.md).  
Covers modularity, scalability, and alignment with best practices for CBVs.

---
## Dependency Management
>  This project includes both `requirements.txt` and `pyproject.toml` for flexibility. You can install dependencies using traditional pip or migrate to modern, editable installs via `pip install --editable .` in the future.


| Feature                             | Benefit                                                          |
| ----------------------------------- | ---------------------------------------------------------------- |
|  **Standardized**                 | Works across build tools (setuptools, poetry, flit, hatch, etc.) |
|  **Cleaner packaging**            | Consolidates all metadata and deps                               |
|  **Tooling config**               | Supports formatter, linters, test runners, etc.                  |
|  **Modern dependency management** | Poetry and pip (PEP 517/518) support it                          |

---
##  AI Use Disclosure
AI tools were used for:
- Drafting CBV logic templates and mixin examples  
- Generating Markdown and APA-style citations  
- Structuring critique sections and discussion summaries  

All AI-assisted outputs were manually verified, revised, and documented in [`docs/AI_LOG.md`](docs/AI_LOG.md).

---

##  References
- Layman, M. (2024). *Understand Django*. Ch. 7–8: Organize with Class-Based Views & Anatomy of an Application. [https://www.mattlayman.com/understand-django](https://www.mattlayman.com/understand-django)  
- Django Documentation: Class-Based Views (https://docs.djangoproject.com/en/stable/topics/class-based-views/)  
- WTAMU CIDM 6325 Course Announcements (Babb, J., 2025)

---

###  Notes
- All tests executed using `python manage.py test`.  
- PR includes combined Module 3 + 4 deliverables.  
- Accessibility and WCAG 2.2 standards maintained throughout forms and templates.
###  Final Validation
- All CBV routes tested manually:
  - `/orders/`, `/order/create/`, `/order/<pk>/update/`, `/order/<pk>/delete/`
- Login/logout flow verified
- Customer creation working via `/customer/create/`
- Templates use Bootstrap 5 and WCAG 2.2 standards
