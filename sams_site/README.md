SAMS site skeleton

This folder contains a minimal Django project skeleton for the SAMS site.

How to run (development):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install Django (and other dependencies) in the venv:

```powershell
pip install django
```

3. Run migrations and start server:

```powershell
cd sams_site
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

4. Visit http://127.0.0.1:8000/ to view the SAMS app index.

Notes
- The project settings are intentionally minimal. For production, set `SAMS_SECRET_KEY` and `DEBUG=False` and configure allowed hosts.
- Extend the `sams` app with your models and features as needed.
