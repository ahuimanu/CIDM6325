# Django project setup with uv (quick notes)

A compact guide for initializing a Django project using `uv` (fast Python package manager) and optional Docker, based on:

- <https://medium.com/@hmbarotov/configuring-a-django-project-with-uv-548f15ccbc63>
- <https://clilog.net/blog/django-project-setup-with-uv-and-docker/>

These steps follow our repo norms: use `uv run` for entry points, `uvx` for ephemeral tools, and Ruff for lint/format. Commands are written for Windows Git Bash.

## TL;DR — one-pass quickstart

```bash
# 0) Install uv (one-time; see https://docs.astral.sh/uv/getting-started/)
# Windows (PowerShell):
# irm https://astral.sh/uv/install.ps1 | iex
# or via pipx:
# pipx install uv

# 1) Create project folder and initialize a Python project
mkdir mysite && cd mysite
uv init  # creates pyproject.toml if you don’t have one

# 2) Pin Python and create a local venv (optional; uv run works without activation)
uv python pin 3.12
uv venv .venv

# 3) Add Django
uv add django

# 4) Create the Django project (in current directory)
uv run django-admin startproject mysite .

# 5) Run migrations and dev server
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000

# 6) Add an app (optional)
uv run python manage.py startapp blog

# 7) Lint/format with Ruff (ephemeral tool via uvx)
uvx ruff check .
uvx ruff check --fix .
uvx ruff format .
```

## Step-by-step with notes

### 1) Install uv

- Prefer the official installer:
  - PowerShell (Windows): `irm https://astral.sh/uv/install.ps1 | iex`
  - macOS/Linux: see docs at `astral.sh/uv`.
- Alternative: `pipx install uv`.
- We avoid global pip installs for app deps; `uv` itself is a global dev tool OK to install once.

### 2) Initialize the project and Python

- `uv init` creates a minimal `pyproject.toml` if you don’t already have one.
- Pinning Python is recommended for reproducibility: `uv python pin 3.12`.
- `uv venv .venv` creates a local virtual environment if you want manual activation.
  - With `uv run`, activation is not required; `uv` ensures deps and runs the command in a managed env.

### 3) Add Django

- `uv add django` writes Django to `pyproject.toml` and installs it.
- Check in `pyproject.toml` and `uv.lock` for deterministic installs.

### 4) Start the Django project

- Inside your repo root: `uv run django-admin startproject mysite .`
  - The trailing `.` puts project files in the current folder.
  - If you prefer a nested layout, omit `.` and move files as needed.
- Common follow-ups:
  - Create an app: `uv run python manage.py startapp blog`
  - Add the app to `INSTALLED_APPS`.

### 5) Run migrations and the dev server

- `uv run python manage.py migrate`
- `uv run python manage.py runserver 0.0.0.0:8000`
  - Binding to `0.0.0.0` is handy for containers/WSL; `127.0.0.1:8000` is fine locally.

### 6) Tooling: Ruff via uvx

- Lint: `uvx ruff check .`
- Format: `uvx ruff format .`
- Add a CI step or pre-commit later if desired; our repo uses Ruff for both lint and format.

## Project structure tips (Django + our norms)

- Apps: consider `apps/<app_name>/` to keep root tidy.
- Templates: per-app `templates/<app_namespace>/…` with namespacing to avoid collisions.
- Environment: read secrets and config from environment, not VCS.
- Tests: use Django’s TestCase (no pytest), keep them close to app code.

## Optional: Docker quickstart with uv

Minimal example to run Django with `uv` in a container. Adjust paths (e.g., `manage.py` location) for your project.

Dockerfile:

```dockerfile
FROM python:3.12-slim
# Install uv (copy mode avoids hardlinks in some FS)
ENV UV_LINK_MODE=copy
RUN pip install --no-cache-dir uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
# Install dependencies into a project-local venv managed by uv
RUN uv sync --frozen --no-editable

# Copy the rest of the app
COPY . .

# Expose Django dev port (optional)
EXPOSE 8000
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Build and run:

```bash
# Build image
docker build -t mysite:dev .
# Run container and map port
docker run --rm -it -p 8000:8000 mysite:dev
```

Notes:

- Check in `uv.lock` to ensure reproducible container builds (`uv sync --frozen`).
- You can bake static collection and migrations into an entrypoint script for prod.

## Troubleshooting

- Command not found: `uv`
  - Ensure it’s on PATH; restart your shell after install.
- `django-admin` not found
  - Use `uv run django-admin …` or `uv run python -m django …`.
- Wrong Python version
  - Re-pin: `uv python pin 3.12` and re-run commands.
- Virtualenv activation
  - Not required with `uv run`. If you prefer activation in Git Bash: `source .venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Unix).

## References

- Configuring a Django project with uv — Medium: <https://medium.com/@hmbarotov/configuring-a-django-project-with-uv-548f15ccbc63>
- Django project setup with uv and Docker — CLI Log: <https://clilog.net/blog/django-project-setup-with-uv-and-docker/>
