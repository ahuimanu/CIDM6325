# CIDM 6325 — Weeks 7–8 (CBV Refactor)

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Implemented
- CBVs for Post CRUD
- PermissionRequiredMixin for publish
- Author ownership enforcement
- Reusable query mixin for search
- Docs in `docs/` per Parts A–E
