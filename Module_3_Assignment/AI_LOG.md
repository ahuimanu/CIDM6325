# AI_LOG – Module 2

This log documents all AI-assisted tasks for Module 2.  
Prompts, outputs, and revisions are recorded for transparency.

| Date       | Prompt / Task | Output Accepted | Revisions / Notes |
|------------|---------------|-----------------|-------------------|
| 2025-09-14 | "Help scaffold CRUD with HTMX in Django" | Yes | Minor field renaming after testing |
| 2025-09-17 | "Draft acceptance criteria for PRD" | Partially | Expanded accessibility requirements |
| 2025-09-18 | "Replace calculate_eta_mock() with AI placeholder logic" | Yes | Code committed, to be refined later |
| 2025-09-20 | "Generate Module 2 PRD draft" | Yes | Used with edits for clarity and compliance |

---

## Module 3 – Part A: Forms, Validation, Auto ID

### 🔧 Feature Implemented
- Added custom validation in `OrderForm` using `clean_order_date`, `clean_order_id`, and `clean()`.
- Refactored `order_id` to be auto-generated using UUID suffix (e.g., "ORD-1A2B3C") via `save()` override in `Order` model.
- Updated `order_form.html` to remove manual `order_id` input and show errors inline with Bootstrap + WCAG-compliant design.
- Enhanced `order_create()` view to show success alert with `order_id` and ETA using HTMX response.

---

### 🤖 Prompt to ChatGPT
> "Can we have the order ID auto-generated alphanumeric starting with ORD?"

---

### ✨ ChatGPT Output Summary
- Recommended removing `order_id` from the form fields.
- Suggested using `uuid.uuid4().hex[:6].upper()` as a unique ID suffix.
- Provided `save()` override logic to assign `order_id` if missing.
- Updated view to show HTMX-based success message with generated `order_id` and calculated ETA.
- Guided HTML updates for `order_form.html` with accessibility best practices.

---

### 🛠 Developer Revisions
- Integrated `calculate_eta_mock(order)` inside `order_create()` to preserve prior logic.
- Preserved `is_update` flag in `order_form.html` to support create/edit reusability.
- Verified error rendering and validation UX for invalid input.

---

### ✅ Outcome
- Streamlined form UX (no manual ID entry)
- Improved consistency and uniqueness of `order_id`
- Boosted accessibility and error feedback compliance (WCAG 2.2)
- Created clear AI documentation trail for reproducibility and transparency

---

### 🧪 Manual Test Notes
- Submitted valid and invalid orders — saw inline field errors as expected
- Verified `order_id` format as `ORD-XXXXXX`
- Confirmed success message showing `order_id` + ETA after HTMX form submission

**Disclosure:**  
All AI-generated suggestions were critically reviewed, tested, and revised before inclusion.  
