## DEPLOYMENT.md – Future Hosting Strategy

**Project:** FinalProject – Logistics Delivery App
**Maintainer:** Mafruha Chowdhury
**Course:** CIDM 6325 – Fall 2025

---

###  Target Platform

Planned hosting on **PythonAnywhere** ([https://www.pythonanywhere.com/](https://www.pythonanywhere.com/))

Alternative platforms considered:

* Render ([https://render.com](https://render.com))
* Railway ([https://railway.app](https://railway.app))
* Azure App Service

---

###  Planned Deployment Steps

1. **Export All Dependencies**

   ```bash
   pip freeze > requirements.txt
   ```

2. **WSGI Configuration**

   * Confirm WSGI application path is set correctly in `logistics_project/wsgi.py`
   * PythonAnywhere will reference this file when running the server

3. **Collect Static Files**

   ```bash
   python manage.py collectstatic
   ```

   * Ensure `STATIC_ROOT` is defined in `settings.py`

4. **Production Settings**

   * `DEBUG = False`
   * `ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']`
   * Add `.env` or environment-safe variable loading (optional)

5. **Database Migration and Superuser**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **PythonAnywhere Web App Configuration**

   * Create a Manual Web App (WSGI mode)
   * Set project path and virtual environment path
   * Point WSGI file to your project’s `wsgi.py`
   * Set static and media mappings (e.g., `/static/`, `/media/`)

7. **Verify Live Site Functionality**

   * [ ] Admin portal loads
   * [ ] File uploads work (ImageField receipt)
   * [ ] ETA logic and HTMX forms operate
   * [ ] CRUD operations successful

---

###  Deployment URL (To be added after launch)

```
https://<yourusername>.pythonanywhere.com
```

Once deployed, update `README.md` with the live site URL and admin test credentials if needed.

---

This deployment file will evolve with the project and serve as a production reference.
