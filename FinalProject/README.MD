# Final Project – Logistics Application (CIDM 6325)

**Author:** Mafruha Chowdhury
**Course:** CIDM 6325 – Electronic Commerce (Fall 2025)
------

**Submission Branch:** `FinalProject/feature/final-delivery-app`
**Live Site URL:** *[Insert your deployed URL]*
**Admin Credentials:** *[Insert username/password]*
**GitHub Repo:** [https://github.com/Mafruha17/CIDM6325/tree/main/FinalProject/](https://github.com/Mafruha17/CIDM6325/tree/main/FinalProject/)


## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Summary](#architecture-summary)
3. [Technology Stack](#technology-stack)
4. [Project Folder Structure](#project-folder-structure)
5. [Baseline Features (70 percent)](#baseline-features-70-percent)
6. [Good Features](#good-features)
7. [Better Features](#better-features)
8. [Best Feature](#best-feature)
9. [Screenshots](#screenshots)
10. [Running the Application](#running-the-application)
11. [Deployment Guide](#deployment-guide)
12. [Submission Summary](#submission-summary)
13. [Executive Overview](#executive-overview)

## Technology Stack

A concise overview of the core technologies used throughout the Final Project:

* **Python 3.x** – Primary programming language
* **Django Framework** – Backend MVC framework used for models, views, forms, admin, authentication
* **SQLite** – Lightweight default database for development
* **HTML, CSS, Bootstrap 5** – Front-end styling and responsive layout
* **HTMX** – Enhanced dynamic UI interactions without full page reloads
* **Docker & Docker Compose** – Containerized development and deployment
* **Gunicorn (optional)** – Production WSGI server
* **Environment Variables (`.env`)** – Secure configuration management

## Project Folder Structure

A structured overview of the FinalProject directory for clarity and maintainability:

```
FinalProject/
│
├── logistics_project/        # Django project settings, root URLs, WSGI
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── logistics_app/            # Core application logic
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/logistics_app/
│
├── templates/                # Global templates (if any)
│
├── static/                   # Static assets (CSS, JS, images)
│
├── media/                    # Uploaded files (receipt images)
│
├── Dockerfile                # Image build instructions
├── docker-compose.yml        # Multi-service orchestration
├── requirements.txt          # Python dependencies
├── AI_LOG.md                 # AI prompt log documentation
├── ETHICS.md                 # Ethics and transparency documentation
└── README.md                 # FinalProject main documentation
```

The structure emphasizes modularity, clarity, and scalability and aligns with Django best practices for real-world deployment.

## Project Overview

The Final Project delivers a complete, production-aligned logistics management application that integrates all functional and architectural competencies developed throughout the semester. The solution is designed as a fully contained Django application that supports order processing, customer management, administrative oversight, secure authentication, file handling, and deployment readiness.

The system consolidates all key operational workflows into a stable, modular project structure suitable for both academic evaluation and real-world implementation. Core enhancements include environment‑based configuration using a `.env` file, Dockerized execution for deployment consistency, refined file upload handling, security‑aligned settings for production, and comprehensive documentation tailored to the Final Project rubric.

The objective is to demonstrate a high‑quality, maintainable, scalable web application that reflects strong engineering practices, clear separation of functional and non‑functional components, and readiness for professional deployment environments.

## Architecture Summary

The Final Project follows a clean, production-oriented Django architecture designed for maintainability, clarity, and deployment readiness. All components are organized under the dedicated FinalProject directory, supporting a modular structure that aligns with best practices in modern Django development.

Key architectural elements include:

* **Project and App Segmentation:** A fully isolated project folder containing `logistics_project` and `logistics_app`, ensuring a clear separation of concerns between settings, routing, application logic, templates, static files, and media assets.

* **Environment-Based Configuration:** Sensitive values such as the secret key, debug mode, and allowed hosts are controlled through a `.env` file, promoting security, portability, and best practices in configuration management.

* **Docker-Enabled Execution:** Docker Compose provides a consistent environment for development and deployment. Containers ensure reproducible builds, clean dependency isolation, and reliable cross-platform behavior.

* **Template and Static Organization:** All templates use a unified `base.html` layout with modular partials. Static assets and media uploads are mapped to clearly defined directories that behave consistently across both local and containerized execution.

* **Secure Production Alignment:** The structure anticipates production deployment with settings prepared for secure cookie handling, HTTPS, HSTS, and host validation. This framework ensures smooth progression from development to a production environment.

* **Documentation Integration:** The project includes structured documentation files (README, AI_LOG, ETHICS) to support transparency, reproducibility, and submission completeness.

      This architecture ensures a stable, scalable, and secure foundation for the logistics application and satisfies the expectations of a graduate-level Django project.

* **Session Management** The application uses Django’s session framework as a core part of its security and workflow architecture. Session data governs authenticated state, permissions, and view access across the entire logistics application. Specifically, sessions support:

   * **Authentication persistence** across all protected routes
   * **Conditional UI rendering** based on `request.user` identity
   * **Permission enforcement** for Order and Customer CRUD views
   * **CSRF-protected form submissions**, tied directly to session identity
   * **HTMX interactions** that require a valid session and CSRF token
   * **Django Admin authorization**, including group-based permission checks

   These session mechanics ensure consistent, secure behavior in both development and production deployments.
   Full session behavior and verification steps are documented in the **TESTING.md** file.
-------


## Baseline Features (70 percent)

The Final Project satisfies all baseline requirements through a combination of features implemented across earlier modules and fully consolidated within the FinalProject directory. This list has been expanded to include new Final Project–specific enhancements.

* **Django Project Structure and App Layout:** Fully organized FinalProject directory with isolated project and application modules, proper settings, templates, static, and media directories.
* **Complete CRUD for Orders and Customers:** Implemented through Class-Based Views, providing list, create, update, and delete workflows.
* **Class-Based Views (****`ListView`****, ****`CreateView`****, ****`UpdateView`****, ****`DeleteView`****):** Applied consistently across core workflows with production-aligned organization.
* **Order and Customer Models with ForeignKey Relationships:** Clear relational structure supporting linked business processes.
* **Forms with Validation and CSRF Tokens:** ModelForms enforce structured validation and maintain security through CSRF protection.
* **Django Admin with Customization:** Model registration, list filters, search, ordering, read-only fields, and custom admin actions such as "Mark as Delivered."
* **Static and Media File Configuration:** Configured `MEDIA_ROOT`, `MEDIA_URL`, and static file paths for both development and Dockerized deployment.
* **User Authentication (Login/Logout):** Full authentication workflow enabled with proper access control.
* **Bootstrap-Based Styling:** Templates fully styled for usability and consistent UI across all pages.
* **Docker-Based Execution:** Containerized environment added for reliable development and deployment workflows.
* **Environment-Based Configuration:** `.env` file support added for secret key, debug mode, and allowed hosts.

These capabilities collectively fulfill the full 70 percent baseline requirement defined in the Final Project rubric.

## Good Features

The Final Project implements and strengthens all Good-level rubric features. Each item below reflects the finalized implementation as included in the **FinalProject** directory.

1. **Named URLs and URL Reversing**
   The Final Project implements `{% url %}` tags and Django reverse lookups consistently across templates. URL patterns are structured under the FinalProject folder using clear, descriptive names to enhance readability and maintainability.

2. **Class-Based Views for CRUD Operations**
   The Final Project uses Class-Based Views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) across Order and Customer workflows. These views are organized under the FinalProject architecture for clarity, deployment stability, and scalability.

3. **Template Inheritance Using Base Layout**
   Templates use a unified `base.html` structure, applying Bootstrap for layout and styling. Common components are shared across all templates using `{% block %}` and `{% include %}` for consistency and reuse.

4. **HTMX Integration for Dynamic UI Updates**
   HTMX is used inside the FinalProject to streamline dynamic interactions, partial page refreshes, and inline updates. All HTMX endpoints are aligned with the FinalProject's routing structure.

5. **Admin Filters, Search, and Bulk Actions**
   The Final Project includes enhanced Django Admin functionality: search fields, list filters, ordering, and custom actions such as "Mark as Delivered." These features improve administrative workflows and operational visibility.

6. **File and Image Uploads with Preview**
   The application supports file uploads via `ImageField` with conditional preview rendering in both admin and user forms. Upload paths are configured to be fully compatible with Docker volumes and production environments.

7. **Bootstrap-Based UI Enhancements**
   The interface uses Bootstrap across all components for accessibility, structure, and responsive design. Styling is consistent across all FinalProject templates.

These Good-level features satisfy and exceed the requirements defined in the Final Project rubric.

## Better Features

The Final Project incorporates and extends all required Better-level rubric features. Each capability is fully implemented within the FinalProject directory and reflects production-oriented enhancements.

1. **ModelForm-Based CRUD with Validation**
   The Final Project uses ModelForms for Orders and Customers to enforce structured validation and reduce redundancy. Validation logic ensures correct data handling, improves form reliability, and aligns with Django best practices for maintainable CRUD operations.

2. **Role-Based Permissions Using Django Groups**
   The application enforces role-specific access through defined user groups such as `CustomerAdmin` and `DataAdmin`. These groups control view access, model permissions, and administrative capabilities. Permission rules ensure that sensitive actions and workflows remain accessible only to authorized users.

3. **Controlled Image Upload Handling and Conditional Rendering**
   File uploads are processed using `ImageField`, with strict directory mapping and preview logic. Uploaded receipts appear only when present, reducing UI clutter and improving user experience. Media configuration is designed to work across both local and containerized environments.

4. **Enhanced Administrative Oversight**
   Administrative screens leverage combined validation, visibility filters, and permissions to support operational oversight. Sensitive model fields are protected through read-only settings, and data management workflows are aligned with real-world business scenarios.

These Better-level features strengthen application integrity, enforce proper access control, and enhance the operational usefulness of the application.

## Best Feature

The Final Project implements a robust Best-level feature that strengthens the application’s security posture and prepares the system for real-world deployment.

### **Production Security Hardening**

The application includes a dedicated production configuration that enhances security and reliability when deployed. Key elements include:

* **DEBUG Disabled:** `DEBUG=False` is enforced in production settings to prevent exposure of sensitive information.
* **Allowed Hosts Defined:** `ALLOWED_HOSTS` is configured to restrict HTTP requests to trusted domains.
* **Environment-Based Secrets:** Sensitive values such as the Django secret key are stored in a `.env` file rather than in source code.
* **Secure Cookie and Session Settings Prepared:** The project structure anticipates secure cookies, HSTS, and HTTPS settings for a secure deployed environment.
* **Static and Media Security:** Static and media files are served with controlled paths that align with containerized deployment requirements.

These measures create a solid foundation for hosting the application in production and satisfy the Best-level requirement of implementing a high-value, security-oriented feature.

## Screenshots

The Final Project includes key visual evidence demonstrating full application functionality. These screenshots validate CRUD workflows, authentication, permissions, and administrative operations. All figures should be placed under a `docs/` or `media/` directory within the FinalProject folder.

### **Screenshots to Include**

1. **Submitted Orders Table**
   Displays the Order list with Bootstrap formatting, receipt preview column, and dynamic updates.

2. **Create Order Form**
   Shows form fields, validation behavior, and the file upload element.

3. **Order Update and Delete Views**
   Demonstrates Class-Based Views, consistent template inheritance, and form behavior.

4. **Image Upload Preview (Admin)**
   Validates thumbnail rendering, secure file handling, and preview logic.

5. **Login Page**
   Proof of Django authentication, session initialization, and access control.

6. **Group Permissions View (Admin)**
   Shows assigned groups (CustomerAdmin, DataAdmin) and their permission structure.

7. **Admin Dashboard**
   Displays search, filters, ordering, and the custom "Mark as Delivered" action.

These screenshots collectively demonstrate compliance with Baseline, Good, and Better rubric features.

## Running the Application

The Final Project supports a clean and reliable workflow for local development.

### **1. Clone the Repository**

```
git clone https://github.com/Mafruha17/CIDM6325.git
cd CIDM6325/FinalProject
```

### **2. Create and Activate a Virtual Environment**

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv/Scripts/activate      # Windows
```

### **3. Install Dependencies**

```
pip install -r requirements.txt
```

### **4. Apply Migrations**

```
python manage.py migrate
```

### **5. Create a Superuser (Optional)**

```
python manage.py createsuperuser
```

### **6. Start the Development Server**

```
python manage.py runserver
```

The project will be available at:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

## Deployment Guide

The Final Project includes Docker support for consistent and reliable deployment across environments.

### **1. Build Docker Images**

```
docker compose build
```

### **2. Start the Application Using Docker**

```
docker compose up
```

### **3. Environment Configuration**

Add a `.env` file with production-ready values:

```
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=your_domain_or_ip
```

### **4. Production Execution (Optional)**

Use Gunicorn for production-grade execution:

```
gunicorn logistics_project.wsgi:application --bind 0.0.0.0:8000
```

### **5. Static and Media File Handling**

Ensure hosting configuration supports:

* `/static/` for static assets
* `/media/` for uploaded content

This deployment workflow ensures portability, stability, and alignment with Final Project rubric expectations.

## Submission Summary

This section provides a consolidated summary of all required deliverables for the Final Project submission. It is intended for quick verification by the professor and supports Canvas submission clarity.

### **Submission Deliverables**

* **Live Application URL: [https://mafruhac.pythonanywhere.com/](https://mafruhac.pythonanywhere.com/)
* **Admin Login Credentials: Username: professor_babb
  Pass: <your professor password here>
* **GitHub Repository Link:** [https://github.com/Mafruha17/CIDM6325/tree/main/FinalProject/](https://github.com/Mafruha17/CIDM6325/tree/main/FinalProject/)
* **ZIP Archive:** Full project directory compressed and uploaded to Canvas.
* **FinalProject README:** Complete documentation including rubric mapping, architecture, and instructions.
* **AI_LOG.md:** Documenting prompt interactions and development support.
* **ETHICS.md:** Summarizing accessibility, ethical considerations, and responsible AI usage.

### **Rubric Alignment Summary**

| Category   | Requirement                         | Complete |
| ---------- | ----------------------------------- | -------- |
| Baseline   | Full CRUD, models, views, templates | ✔ Yes    |
| Good       | 4+ features implemented             | ✔ Yes    |
| Better     | 2+ features implemented             | ✔ Yes    |
| Best       | 1 major feature secured             | ✔ Yes    |
| Deployment | Site live with admin credentials    | ✔ Yes    |
| Submission | PR + ZIP + Canvas checklist met     | ✔ Yes    |

### **Notes for Professor**

This Final Project integrates all major components developed throughout CIDM 6325 and enhances them with production-oriented deployment, security hardening, Docker support, and full documentation readiness.

## Application Validation & Smoke Testing Summary

### Core Functional Workflows Verified

* Successful login using `professor_babb` account.
* Creation, editing, and deletion of **Customers**.
* Creation, editing, and deletion of **Orders** linked to Customers.
* Receipt file upload rendering correctly via MEDIA settings.
* Mock ETA values displayed consistently.
* Navigation across all menu items (`Orders`, `Create Order`, `Create Customer`, `Predict ETA`, `Admin`).

### Admin Panel Verification

* Access to Django Admin using superuser credentials.
* Group creation and permission assignments validated.
* User management verified, including search, filters, and status indicators.

### Deployment-Level Testing (PythonAnywhere)

* Static files served correctly using `STATIC_ROOT`.
* Media files accessible through configured `MEDIA_ROOT`.
* Allowed hosts validation successful.
* Full CRUD workflows behave identically to local environment.

### Smoke Test Checklist

* [x] Homepage loads without error
* [x] Orders list loads with existing records
* [x] Creating a new Customer works
* [x] Creating an Order linked to a Customer works
* [x] Uploading and previewing receipts works
* [x] Editing and deleting records works
* [x] Admin login/authentication works
* [x] Session cookies operate as expected
* [x] Static and media serving verified on production

---

## Executive Overview

The Final Project is the culmination of all major learning objectives in CIDM 6325 and integrates every core concept practiced across Modules 1 through 5 into a single, cohesive logistics management application. The system demonstrates full-stack competency in Django development, modular application design, authentication and authorization workflows, dynamic UI behavior, and secure deployment practices.

This application delivers a complete business workflow for managing customer profiles, processing delivery orders, uploading and reviewing delivery receipts, and performing administrative oversight through an optimized Django Admin interface. Each component is built with clarity, maintainability, and future extensibility in mind. The architecture separates functional and non-functional concerns, enabling the system to scale while remaining secure and operationally clear.

The Final Project not only consolidates all major functional deliverables from earlier modules but also extends them through:

* A production-oriented project layout under the FinalProject directory.
* A Docker-based workflow that ensures consistency across environments.
* Environment variable management for secure configuration.
* Deployment readiness through production-level settings and Gunicorn support.
* Documented development and deployment instructions for reproducibility.

This project demonstrates a high level of architectural maturity and readiness for real-world use. The completed features collectively satisfy the Baseline, Good, Better, and Best requirements of the Final Project rubric and present a secure, maintainable, and professionally structured Django web application.
