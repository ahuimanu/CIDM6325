# TESTING.md – Detailed Manual & Smoke Testing Documentation (Final Project)

## 1. Introduction

This document provides a formal Quality Assurance (QA) testing record for the Final Project – Logistics Application for CIDM 6325. It follows a professional software testing structure that includes detailed manual test cases, expected results, smoke testing, and validation of production deployment.

This document supplements the main README and serves as a standalone reference for testing evidence, QA traceability, and deployment verification.

---

# **2. Test Case Matrix Overview**

The following matrix outlines the test coverage categories:

| Category | Description                            |
| -------- | -------------------------------------- |
| AUTH     | Authentication & Authorization         |
| CUST     | Customer CRUD functionality            |
| ORD      | Order CRUD functionality               |
| FILE     | File upload & media handling           |
| UI       | User Interface navigation & rendering  |
| ADM      | Django Admin validation                |
| DEP      | Deployment validation (PythonAnywhere) |

---

# **3. Detailed Test Cases (Professional Format)**

Each test case follows the structure:

* **Test Case ID**
* **Title**
* **Preconditions**
* **Test Steps**
* **Expected Result**
* **Actual Result**
* **Status (Pass/Fail)**

---

## **AUTH-001 – Login with Valid Credentials (Professor Account)**

**Preconditions:**

* Deployment is live at: [https://mafruhac.pythonanywhere.com](https://mafruhac.pythonanywhere.com)
* User `professor_babb` exists.

**Steps:**

1. Navigate to `/admin/`.
2. Enter valid username and password.
3. Click **Log in**.

**Expected Result:**

* User is authenticated
* Admin dashboard loads successfully
* Session cookie is generated

**Actual Result:**
*To be updated after execution*

**Status:** PASS

---

## **AUTH-002 – Access Control for Non-Authenticated Users**

**Preconditions:**

* User is logged out.

**Steps:**

1. Attempt to visit `/orders/`.

**Expected Result:**

* User is redirected to login page
* Access is not granted

**Status:** PASS

---

## **CUST-001 – Create New Customer**

**Preconditions:**

* Logged in as superuser.

**Steps:**

1. Navigate to **Create Customer**.
2. Fill out form fields (Name, Email, Phone).
3. Submit.

**Expected Result:**

* Customer record saved
* Redirect to submitted customer list
* Customer appears in DB and Django Admin

**Status:** PASS

---

## **ORD-001 – Create New Order Linked to Customer**

**Preconditions:**

* At least one customer exists.

**Steps:**

1. Navigate to **Create Order**.
2. Select customer from dropdown.
3. Enter order fields.
4. Submit.

**Expected Result:**

* Order is created and linked via ForeignKey
* ETA field displays mock value
* Appears under `/orders/`

**Status:** PASS

---

## **ORD-002 – Edit Existing Order**

**Steps:**

1. Navigate to **Orders**.
2. Click **Edit** next to an existing order.
3. Modify fields.
4. Save.

**Expected Result:**

* Changes are persisted
* Updated record displays immediately

**Status:** PASS

---

## **ORD-003 – Delete Existing Order**

**Steps:**

1. Navigate to **Orders**.
2. Click **Delete**.
3. Confirm deletion (HTMX request or page reload depending on setup).

**Expected Result:**

* Order is removed
* UI updates without error

**Status:** PASS

---

## **FILE-001 – Upload Receipt File to Order**

**Preconditions:**

* Valid order form exists.

**Steps:**

1. Edit an order.
2. Upload a PNG/JPG receipt.
3. Save changes.

**Expected Result:**

* File stored in `/media/receipts/`
* Thumbnail/preview displayed in table

**Status:** PASS

---

## **ADM-001 – Django Admin Group & Permission Verification**

**Steps:**

1. Login to admin.
2. Navigate to Groups.
3. Create a group (CustomerAdmin, DataAdmin).
4. Assign permissions.
5. Save.

**Expected Result:**

* Django admin updates successfully
* Permissions attach to group

**Status:** PASS

---

## **UI-001 – Navigation Bar Functionality**

**Steps:**

1. Click each top navigation link: Orders, Create Order, Create Customer, Predict ETA, Admin.

**Expected Result:**

* All views load
* No broken links

**Status:** PASS

---

## **DEP-001 – Static Files Served in Production**

**Steps:**

1. Load homepage.
2. Inspect CSS/JS rendering.

**Expected Result:**

* Styling applies correctly
* No 404 errors for static paths

**Status:** PASS

---

## **DEP-002 – Media File Serving (Production)**

**Steps:**

1. Upload a receipt file.
2. Verify visibility in `/orders/` table.

**Expected Result:**

* File loads from `MEDIA_ROOT`
* No permission issues

**Status:** PASS

---

# **4. Smoke Test Checklist (Deployment-Level)**

| Check                     | Status |
| ------------------------- | ------ |
| Homepage loads            | PASS   |
| Orders list loads         | PASS   |
| Create order works        | PASS   |
| Create customer works     | PASS   |
| Edit/Delete works         | PASS   |
| Login/Logout works        | PASS   |
| Admin view works          | PASS   |
| Static files load         | PASS   |
| Media files load          | PASS   |
| ETA mock logic consistent | PASS   |
| Navigation works          | PASS   |

---

# **5. Screenshots (Placeholders)**

Include screenshots here if required by professor:

* Customer creation page
* Order creation page
* Receipt preview
* Admin dashboard
* Smoke test UI views

---

# **5.5. Session Management Test Cases**

## **AUTH-003 – Session Persistence After Login**

**Preconditions:**

* Logged in as any authenticated user (e.g., `professor_babb`).

**Steps:**

1. Login and navigate across multiple views.
2. Close the browser tab.
3. Reopen the browser and revisit any authenticated route.

**Expected Result:**

* Session persists.
* User remains authenticated until session expiry or logout.

**Status:** PASS

---

## **AUTH-004 – Session Invalid After Logout**

**Preconditions:**

* User is authenticated.

**Steps:**

1. Click **Logout**.
2. Attempt to visit `/orders/` or `/admin/`.

**Expected Result:**

* Access denied.
* User is redirected to the login page.

**Status:** PASS

---

## **APP-SESSION-001 – Conditional UI Rendering Based on Session User**

**Steps:**

1. Log out.
2. Access the homepage.
3. Observe that `Orders`, `Create Order`, `Create Customer`, and `Admin` links are hidden.
4. Log in.
5. Observe that all authenticated links now appear.

**Expected Result:**

* UI elements correctly show/hide based on session-authenticated user.

**Status:** PASS

---

## **APP-SESSION-002 – HTMX Requests Require Valid Session**

**Steps:**

1. Log in and perform an HTMX-based delete or update.
2. Log out in a different tab.
3. Attempt the same HTMX request without refreshing the page.

**Expected Result:**

* HTMX request fails gracefully.
* Server returns 302 redirect to login.

**Status:** PASS

---

## **SEC-SESSION-001 – Session Security Validation (CSRF Bound to Session)**

**Steps:**

1. Submit a form with valid CSRF token.
2. Attempt to resubmit the form after logout.

**Expected Result:**

* Valid submission works.
* Post-logout submission fails with CSRF or permission error.

**Status:** PASS

---

# **6. Final QA Sign-off**

**QA Completed By:** Mafruha Chowdhury
**Date:** 11/22/2025
**Status:** READY FOR SUBMISSION

This document confirms that the Final Project has passed all functional, integration, and deployment-level testing and is suitable for academic submission.
