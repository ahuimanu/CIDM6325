## ETHICS.md – Accessibility, Security & Responsible AI Use

**Author:** Mafruha Chowdhury
**Course:** CIDM 6325 – Fall 2025
**Project:** Logistics Delivery App – FinalProject

---

### ♾ Accessibility Practices

| Area                  | Implementation                                                                |
| --------------------- | ----------------------------------------------------------------------------- |
| Form Design           | All forms follow Bootstrap 5 accessibility standards with label-input linking |
| Screen Reader Support | ARIA roles and clear `alt` text on file upload previews                       |
| Keyboard Navigation   | Bootstrap-based controls support tabbing and focus styling                    |
| Error Feedback        | Form validation messages are visually distinct and screen-reader accessible   |

---

###  Security Practices

| Area                   | Control Implemented                                                            |
| ---------------------- | ------------------------------------------------------------------------------ |
| Authentication         | Django's built-in `LoginView` and `LoginRequiredMixin` enforce auth boundaries |
| Authorization          | Role-based group permissions: `CustomerAdmin`, `DataAdmin`                     |
| File Upload Protection | `ImageField` upload paths restricted to authenticated users only               |
| Media Access Isolation | Uploaded receipts restricted via server-side permission checks                 |
| Production Hardening   | `DEBUG=False`, secure headers, static/media handling in deployment             |

---

###  Ethical Use of AI

* AI tools (ChatGPT-4) were used to **enhance structure, not replace development judgment**
* Generated code was always reviewed, customized, and validated against Django documentation
* No confidential or proprietary data was exposed to AI models

---

###  Academic Integrity

This file supports the CIDM 6325 requirement for transparency in AI and ethics. No content was reused from prior semesters. All logic was written or reviewed specifically for Fall 2025.

Prompt history and technical rationale are provided in `AI_LOG.md`.

---

**This ethics log reflects responsible, transparent software development and meets the expectations of WTAMU’s academic integrity policies.**
