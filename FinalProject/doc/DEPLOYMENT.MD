# FinalProject: Logistics Delivery App Final Build

**Author:** Mafruha Chowdhury
**Course:** CIDM 6325 – Electronic Commerce (Fall 2025)
**Submission Branch:** `FinalProject/feature/final-delivery-app`
**GitHub Repo:** [CIDM6325 FinalProject](https://github.com/Mafruha17/CIDM6325/tree/main/FinalProject/)

---

## ✅ Project Feature Checklist per Rubric

### Baseline (All Met)

* Django project structure with CRUD
* Class-Based Views: `ListView`, `CreateView`, `UpdateView`, `DeleteView`
* `Order` and `Customer` models with FK
* Forms with validation and CSRF protection
* Django admin integration
* Static/media files handling (`STATICFILES_DIRS`, `MEDIA_ROOT`)
* User authentication (login/logout)
* Bootstrap-styled layout

### Good Features

* Named URL routing with `{% url %}`
* Template inheritance with `base.html`
* HTMX integration (delete + inline refresh)
* Admin filters, search, bulk actions
* Image upload + preview in admin

### Better Features

* `ModelForm` with validation
* Role-based groups (`CustomerAdmin`, `DataAdmin`, etc.)
* Conditional image rendering

### Best Feature

**Group-Based File Upload Restriction**

* Media uploads under `/media/receipts/`
* Access restricted to authenticated staff/admin users

---

## 🧱 Architecture Summary

* App: `logistics_app/`
* Project: `logistics_project/`
* Modular: `models.py`, `views.py`, `forms.py`, `urls.py`
* Templates in: `templates/logistics_app/`
* Static assets in: `static/`
* Media uploads: `/media/`

---

## 🧪 Testing Overview

Tested with `coverage.py`:

```bash
coverage run manage.py test
coverage html
```

**Coverage:** ~79%

| Module    | Coverage |
| --------- | -------- |
| views.py  | 82%      |
| models.py | 75%      |
| forms.py  | 52%      |
| admin.py  | 88%      |

Reports viewable at `htmlcov/index.html`

---

## 🚀 Docker Setup (Local Dev)

### Prerequisites

* Docker Desktop installed
* VSCode with Docker extension (optional)

### .dockerignore

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
*.db
*.sqlite3
staticfiles/
media/
.DS_Store
```

### Run via Docker Compose

```bash
docker compose up --build
```

* App runs at: [http://localhost:8000](http://localhost:8000)
* Admin: [http://localhost:8000/admin](http://localhost:8000/admin)

### Switch to Production (Later)

To switch from `runserver` to `gunicorn`, update the `web:` block in `docker-compose.yml`:

```yaml
command: >
  sh -c "python manage.py collectstatic --noinput && \
         gunicorn logistics_project.wsgi:application --bind 0.0.0.0:8000"
```

---

## 🖥️ Local Manual Setup (No Docker)

```bash
# Clone and setup
cd CIDM6325/FinalProject
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🗂️ Linked Docs

* [`AI_LOG.md`](./doc/AI_LOG.MD)
* [`ETHICS.md`](./doc/ETHICS.md)
* [`DEPLOYMENT.md`](./doc/DEPLOYMENT.md)

---

## 📊 Submission Summary

| Category   | Met? |
| ---------- | ---- |
| Baseline   | ✅    |
| Good       | ✅    |
| Better     | ✅    |
| Best       | ✅    |
| Deployment | ✅    |
| Submission | ✅    |

---

## 📸 Screenshots Checklist (To Add Later)

* Submitted Orders Table
* Create Order Form
* HTMX Deletion
* Image Upload Preview
* Login Page
* Admin Group Permissions View
