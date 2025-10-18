# AI_LOG – Module 2, 3, and 4

This log documents all AI-assisted tasks for Modules 2, 3, and 4.  
Prompts, outputs, and revisions are recorded for transparency.

---

##  Module 2 – Logistics Platform HTMX & AI ETA

| Date       | Prompt / Task | Output Accepted | Revisions / Notes |
|------------|---------------|-----------------|-------------------|
| 2025-09-14 | "Help scaffold CRUD with HTMX in Django" | Yes | Minor field renaming after testing |
| 2025-09-17 | "Draft acceptance criteria for PRD" | Partially | Expanded accessibility requirements |
| 2025-09-18 | "Replace calculate_eta_mock() with AI placeholder logic" | Yes | Code committed, to be refined later |
| 2025-09-20 | "Generate Module 2 PRD draft" | Yes | Used with edits for clarity and compliance |

---

##  Module 3 – Forms, Validation, Auto ID

###  Feature Implemented
- Added custom validation in `OrderForm` using `clean_order_date`, `clean_order_id`, and `clean()`.
- Refactored `order_id` to be auto-generated using UUID suffix (e.g., "ORD-1A2B3C") via `save()` override in `Order` model.
- Updated `order_form.html` to remove manual `order_id` input and show errors inline with Bootstrap + WCAG-compliant design.
- Enhanced `order_create()` view to show success alert with `order_id` and ETA using HTMX response.

###  Prompt to ChatGPT
> "Can we have the order ID auto-generated alphanumeric starting with ORD?"


### 🛠 Developer Revisions
- Integrated `calculate_eta_mock(order)` inside `order_create()` to preserve prior logic.
- Preserved `is_update` flag in `order_form.html` to support create/edit reusability.
- Verified error rendering and validation UX for invalid input.

###  Outcome
- Streamlined form UX (no manual ID entry)
- Improved consistency and uniqueness of `order_id`
- Boosted accessibility and error feedback compliance (WCAG 2.2)
- Created clear AI documentation trail for reproducibility and transparency

###  Manual Test Notes
- Submitted valid and invalid orders — saw inline field errors as expected
- Verified `order_id` format as `ORD-XXXXXX`
- Confirmed success message showing `order_id` + ETA after HTMX form submission

**Disclosure:**  
All AI-generated suggestions were critically reviewed, tested, and revised before inclusion.

---

##  Module 4 – CBV Refactor, Architecture Critique, Testing

###  Features Implemented
- Refactored `OrderListView`, `OrderCreateView`, `OrderUpdateView`, and `OrderDeleteView` into Django CBVs.
- Used `LoginRequiredMixin`, `SuccessMessageMixin`, and `reverse_lazy`.
- Replaced FBVs in `logistics_app/views.py`.
- Created `test_views_cbv.py` to verify status codes, template rendering, and redirects.
- Helped draft FBV vs CBV comparison and modularity notes for `README.md`.

###  Prompts to ChatGPT
> “Refactor Django CRUD views from FBV to CBV using LoginRequiredMixin and SuccessMessageMixin”   
> “Explain tradeoffs between FBVs and CBVs for `README.md` section”

###  ChatGPT Output Summary
- Provided modular CBV scaffolding with mixins and inheritance.
- Rewrote CRUD views using Django generics and mapped templates.t.
- Drafted FBV vs CBV summary discussing maintainability, inheritance, and route mapping.

###  Developer Revisions
- Replaced hardcoded URLs with `reverse_lazy` for safer routing.
- Modified context data and method overrides for clarity.
- Adjusted URLs and ensured integration with existing templates.

###  Outcome
- Functional CBV CRUD system aligned with best practices.
- Tests ensure routing and template integrity.
- Clean documentation of AI involvement and testing coverage.

###  Manual Test Notes
- All four views tested with sample orders and status checks.
- CRUD flow verified: list → create → update → delete → redirect.
- Templates rendered correctly; admin links tested.

**Disclosure:**  
All AI-generated code and explanations were carefully reviewed, revised, and tested before inclusion.  
Documented here for transparency and reproducibility.

---

**End of AI_LOG.md**
