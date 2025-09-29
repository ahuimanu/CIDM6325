  Product Requirements Document (PRD): ExpenseTrack-Lite

 Abstract   
As a beginner in web development, I'm creating ExpenseTrack-Lite, a straightforward web application designed to assist individuals such as students or young professionals in monitoring their daily expenditures, including items like meals or transportation. Utilizing Django for backend management, Bootstrap for an intuitive interface, and HTMX for seamless interactions, this document outlines the essential requirements for a minimal viable artifact (MVA) that I can complete within two weeks. This aligns with the objectives of CIDM 6325, emphasizing AI-assisted coding and portfolio-building. The app prioritizes accessibility, adhering to basic WCAG guidelines, to ensure inclusivity for all users.

---

   1. Introduction

-  Context and Vision : ExpenseTrack-Lite is my introductory project in the CIDM 6325 course, aimed at learning foundational web development skills through a practical application. It envisions a simple tool that empowers users to log and review expenses effortlessly, fostering better financial habits without the complexity of commercial apps.
-  Problem Statement : Many individuals, particularly students and early-career professionals, find it challenging to track daily spending due to disorganized records and overly intricate budgeting tools, often resulting in financial oversight. This app provides an accessible, cost-free solution to log and summarize expenses, promoting informed budgeting decisions.
-  Goals :
  - Enable efficient addition, viewing, editing, and deletion of expenses.
  - Develop a user-friendly prototype within a two-week timeframe for portfolio purposes.
  - Incorporate accessibility features to broaden usability.
  - Document AI usage in development to enhance learning transparency.
-  Link to Strategy : This project supports the course's focus on AI-native, portfolio-driven development, applying concepts from Django's views and templates as discussed in the assigned readings.

---

   2. Objectives and Success Metrics

-  Objectives :
  - Facilitate quick expense logging and review to aid daily budgeting.
  - Construct a functional beginner-level app demonstrating core web technologies.
  - Ensure compliance with basic accessibility standards for inclusive design.
-  Success Metrics :
  - Successful logging and retrieval of at least 10 expenses in testing sessions.
  - 100% completion rate for CRUD operations without errors.
  - Inclusion of at least five documented AI prompts with reflections.
  - Achievement of 90% compliance in accessibility checks using tools like WAVE.

---

   3. Scope

-  Features Included :
  - CRUD operations for expenses, capturing date, description, amount, and category (e.g., "Food" or "Transport").
  - Responsive forms via Bootstrap with real-time updates powered by HTMX.
  - A summary view displaying total expenditures overall and by category.
  - AI-assisted code generation, logged for transparency.
  - Basic accessibility validations to meet WCAG criteria.
-  Out of Scope :
  - User authentication or multi-user capabilities.
  - Advanced visualizations such as charts or graphs.
  - Integrations with external services like financial APIs.
  - Specialized mobile optimizations beyond standard responsiveness.

---

   4. User Stories & Use Cases

-  User Stories :
  - As a student, I want to add an expense promptly, so that I can maintain an accurate record of my spending.
  - As a user, I want to view a list of my expenses, so that I can assess my financial patterns.
  - As a user, I can edit or delete an expense, so that I can correct inaccuracies.
  - As a novice developer, I want to log AI prompts, so that I can reflect on my learning process.
-  Use Cases :
  -  Happy Path : A user enters a $10 transportation expense, views it in the list, and reviews the weekly total.
  -  Edge Case 1 : Entry of an invalid (negative) amount triggers a user-friendly error message.
  -  Edge Case 2 : Attempting to delete a non-existent expense is handled gracefully without system failure.

---

   5. Functional Requirements

-  FR-001 : The application must permit creation of an expense entry with fields for date, description, amount, and category.
-  FR-002 : The application must display a sortable list of expenses by date or amount.
-  FR-003 : The application must support editing and deletion of expenses with immediate HTMX updates.
-  FR-004 : The application must provide aggregated totals for overall and category-specific spending.
-  Prioritization : All requirements are classified as "Must Have" to establish a core functional prototype.

---

   6. Non-Functional Requirements

-  Performance : Operations such as adding or viewing expenses should complete in under 2 seconds for up to 100 entries.
-  Scalability : Designed for single-user operation with capacity for up to 500 expenses in a local database.
-  Accessibility : Conforms to WCAG 2.1 Level A guidelines, including keyboard navigation and color contrast.
-  Security/Compliance : Limits data to non-sensitive expense details, with no external transmission.
-  Reliability/Availability : Maintains operational stability during local development and testing.

---

   7. Dependencies & Risks

-  Dependencies :
  -  Internal : Django (current version), Python 3.10+, and SQLite database.
  -  External : Bootstrap and HTMX libraries via CDN.
  -  Cross-Team : None, as this is an individual beginner endeavor.
-  Risks :
  -  AI-Generated Errors : Potential inaccuracies in AI-suggested code.  Mitigation : Document prompts and perform manual validations.
  -  Accessibility Shortfalls : Incomplete adherence to standards.  Mitigation : Leverage Bootstrap's accessible elements and verify with WAVE.
  -  Scope Expansion : Risk of incorporating non-essential features.  Mitigation : Adhere strictly to defined scope and note boundaries in documentation.
-  Assumptions :
  - Users possess basic web browsing proficiency.
  - Development environment is configured per course guidelines.
  - AI tools yield actionable code with minor adjustments.

---

   8. Acceptance Criteria

-  FR-001 : Validated when an expense is added with complete fields and persists in the database.
-  FR-002 : Validated when a list of 10 expenses is displayed and sorted correctly.
-  FR-003 : Validated when edits or deletions update the interface instantly via HTMX.
-  FR-004 : Validated when totals accurately reflect aggregated data by category.
-  Accessibility : Validated when WAVE assessments indicate no major WCAG Level A issues.

---

   AI Disclosure

-  Prompt 1 : "Provide a Django model for an expense tracker including date, description, amount, and category fields."  
  -  Output Accepted : Standard model definition with appropriate fields.  
  -  Revisions : Incorporated validation for non-negative amounts and predefined category options.  
-  Prompt 2 : "Design a Bootstrap form for expense entry in Django."  
  -  Output Rejected : Lacked essential accessibility features such as labels.  
  -  Revisions : Enhanced with ARIA attributes and WCAG-aligned elements from Bootstrap resources.  
-  Prompt 3 : "Supply HTMX code for updating an expense list without page reload."  
  -  Output Accepted : Effective snippet for dynamic edits.  
  -  Revisions : Streamlined for compatibility with Django views and beginner comprehension.  
-  Prompt 4 : "Describe methods to enhance Django views for screen reader accessibility."  
  -  Output Accepted : Advice on semantic HTML and ARIA implementation.  
  -  Revisions : Applied to templates, ensuring keyboard support as per Layman's Chapter 4.  
-  Prompt 5 : "Recommend a basic approach to compute expense totals in Django."  
  -  Output Accepted : Example using QuerySet aggregation.  
  -  Revisions : Extended to include category grouping and verified for precision.  

 Figure 1: System Architecture for ExpenseTrack-Lite   
*Caption*: Illustrates the integration of Bootstrap and HTMX in the front-end with Django's back-end processing and SQLite storage, supported by AI in code development.

---

   References

- Forbes Advisor. (2025). *The Benefits Of Expense Tracking And How You Can Do It Effectively*. <https://www.forbes.com/sites/truetamplin/2025/01/15/the-benefits-of-expense-tracking-and-how-you-can-do-it-effectively/>
- Equifax. (n.d.). *Budgeting Apps: What Are They & How They Work*. <https://www.equifax.com/personal/education/personal-finance/articles/-/learn/budgeting-apps/>
- Plain English. (2024). *Building an Expense Tracker Using Django*. <https://python.plainenglish.io/building-an-expense-tracker-using-django-bb8239537815>
- W3C. (2025). *Web Content Accessibility Guidelines (WCAG) 2.1*. <https://www.w3.org/TR/WCAG21/>
- Layman, M. (n.d.). *Understand Django: Views On Views (Chapter 3)*. <https://www.mattlayman.com/understand-django/>
- Layman, M. (n.d.). *Understand Django: Templates For User Interfaces (Chapter 4)*. <https://www.mattlayman.com/understand-django/>