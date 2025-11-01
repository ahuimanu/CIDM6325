## 📄 ✅ Module 5 – CIDM 6325: Django Admin + Authentication

*Author: Mafruha Chowdhury*
*Course: CIDM 6325 – Electronic Commerce (Fall 2025)*
*Focus: Django Admin, Authentication, Role Permissions, File Uploads*

---

### ✅ **Table of Contents**

1. [Overview](#overview)
2. [Part A – Django Admin Implementation](#part-a)
3. [Part B – Authentication + Role-Based Permissions](#part-b)
4. [Part C – Peer Review](#part-c)
5. [Part D – Blog Post: Productivity vs Security](#part-d)
6. [Part E – Static and Uploaded Files](#part-e)
7. [AI Use Disclosure](#ai-use-disclosure)
8. [References](#references)

---

### 🔍 **Overview**

This module builds on previous assignments by enhancing the Django Admin experience, implementing user authentication with role-based permissions, and supporting file uploads with image previews.

---

## 🧹 <a name="part-a"></a>**Part A – Django Admin Implementation**

Customized Django admin views for two models:

| Model   | Admin Customizations |
| ------- | -------------------- |
| `Order` |                      |

* `list_display`: order_id, date, client type, delivery location, receipt preview
* `list_filter`, `search_fields`, and `readonly_fields`
* Custom admin action: **Mark as Delivered**
* Dynamic "Create Order" button  |
  | `Customer` |
* `list_display`: name, email, phone, and **View Orders** link
* `search_fields` + `ordering`
* Connected to order via `related_name="orders"`  |

#### 💼 Business Use Case

Back-office and customer service roles can:

* Search/filter records
* Perform bulk updates
* View related orders for customers
* Initiate order entry directly from admin panel

---

## 🔐 <a name="part-b"></a>**Part B – Authentication + Role-Based Permissions**

Implemented Django authentication system using:

* Built-in login/logout views
* Password strength enforcement
* Superuser and staff user management via Admin

Created and tested groups:

* `CustomerAdmin_WTAMU_S`
* `DataAdmin`
* `DevTestAccounts`

Permissions assigned via admin UI (`/admin/auth/group/`) to limit or grant:

* Add/view/delete Orders
* Add/view/edit Customers

#### 🧪 Tested Behavior

* Different users in different groups had varying access
* Admins could manage records, others were limited
* Secure login, logout, and access control confirmed

---

## 🖼️ <a name="part-e"></a>**Part E – Static and Uploaded Files**

### 🔧 Tech Stack:

* `ImageField` added to `Order` model (`delivery_receipt`)
* Configured `MEDIA_URL` and `MEDIA_ROOT` in `settings.py`
* Enabled upload handling in `order_form.html` using `enctype="multipart/form-data"`

### 🧲 Frontend Behavior

* Users can attach a receipt file (image/pdf) when creating or editing orders
* Uploaded files stored under `media/receipts/`
* Files previewed inline in the order list using `img-thumbnail`
* "No file" displayed if none uploaded

### 📈 Figure Captions and Visual Evidence (To Be Finalized)

* ☑️ Screenshot: Order form with file upload input (Create/Edit view)
* ☑️ Screenshot: Uploaded receipt image rendered in Submitted Orders table
* ☑️ Screenshot: Django Admin - Uploaded file preview + customer linkage
* ☑️ Screenshot: Static vs Uploaded file routing (Settings/URL config)

---

## 🤖 <a name="ai-use-disclosure"></a>**AI Use Disclosure**

AI tools (ChatGPT-4o) were used for:

* Writing and validating `admin.py`, `forms.py`, `models.py`
* Generating `README.md` structure and documentation
* Designing the UX for file upload and role-based access
* All outputs reviewed and tested before use

---

## 📚 <a name="references"></a>**References**

* Layman, M. (2024). *Understand Django*. Chapters 9 & 11
* Django Documentation – [https://docs.djangoproject.com](https://docs.djangoproject.com)
* WTAMU CIDM 6325 Course Materials (Dr. Jeffry Babb, Fall 2025)

---

(*Parts C and D in progress – will be added next*)
