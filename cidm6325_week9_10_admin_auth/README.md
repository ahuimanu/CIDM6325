# CIDM 6325 — Weeks 9–10: Django Admin, Auth, and Uploads

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## What’s implemented
- Django Admin enabled with customized ModelAdmins for Category, Tag, Post, Comment
- Registration, login, logout; role-based permission `blog.can_publish`
- Image uploads on Post with MEDIA config; templates render thumbnails/full images
- Docs in `docs/` mapped to Parts A–E

## Production notes
- Use DEBUG=False, configure ALLOWED_HOSTS, HTTPS, secure cookies, and a persistent storage for media uploads.
- Add file validation and size limits for uploads.
