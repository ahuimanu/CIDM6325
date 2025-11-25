# Tutorial: ADR-1.0.8 — Settings configuration and secrets

This comprehensive tutorial teaches the implementation of environment-based configuration for Django applications. It follows ADR-1.0.8 and the corresponding briefs, providing step-by-step instructions with embedded Django documentation context, complete code examples, and detailed verification steps.

## Goals and context

**ADR**: `docs/travelmathlite/adr/adr-1.0.8-settings-configuration-and-secrets.md`  
**Briefs**: `docs/travelmathlite/briefs/adr-1.0.8/`

**Goal**: Split Django settings into environment-specific modules (`base`, `local`, `prod`), load configuration from environment variables using `django-environ`, enforce secure production defaults with WhiteNoise integration, and provide comprehensive documentation and automated tests.

**Why this matters**: Production and development environments have different requirements. Development needs debugging tools and convenience; production needs security hardening and performance optimization. Separating these concerns into distinct settings modules following the 12-factor app methodology makes deployments safer and more maintainable.

## Prerequisites

- **Environment**: Python 3.13, virtualenv activated
- **Tooling**: `uv` package manager available
- **Repository**: Branch `FALL2025`, project root at `C:/Users/Jeff/source/repos/courses/CIDM6325`
- **Django knowledge**: Basic familiarity with Django settings, management commands, and environment variables

**Activate your virtualenv before running commands**:

```bash
source .venv/Scripts/activate  # Windows bash-style
```

**Repository state note**: This tutorial assumes the following files will be created:

- `travelmathlite/core/settings/__init__.py` — Settings package initialization
- `travelmathlite/core/settings/base.py` — Shared settings with django-environ
- `travelmathlite/core/settings/local.py` — Development settings
- `travelmathlite/core/settings/prod.py` — Production settings with security hardening
- `travelmathlite/.env.example` — Environment variable template
- `travelmathlite/core/tests/test_settings_local.py` — Local settings tests
- `travelmathlite/core/tests/test_settings_prod.py` — Production settings tests
- `docs/travelmathlite/ops/settings.md` — Operations documentation

---

## Section 1 — Settings split (base/local/prod)

**Brief**: `docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-01-settings-split.md`

### Brief context and goal

Split Django's monolithic `settings.py` into a settings package with three modules:

- **base.py**: Shared configuration used by all environments
- **local.py**: Development overrides (DEBUG=True, permissive settings)
- **prod.py**: Production hardening (DEBUG=False, security enforcement)

This separation makes environment-specific behavior explicit and prevents accidentally deploying development settings to production.

### Relevant Django concepts

#### Django settings as a Python module

From the Django documentation:

> A settings file is just a Python module with module-level variables. Django's configuration system imports your settings module and reads its module-level variables. The `DJANGO_SETTINGS_MODULE` environment variable tells Django which settings module to import.

**Key concept**: Django loads settings by importing a Python module. The `DJANGO_SETTINGS_MODULE` environment variable specifies which module:

```bash
# Development
export DJANGO_SETTINGS_MODULE=core.settings.local

# Production  
export DJANGO_SETTINGS_MODULE=core.settings.prod
```

When not set, Django looks for `settings.py` in your project root.

#### Settings inheritance pattern

From Matt Layman's "Understand Django":

> A common pattern for managing multiple environments is to have a base settings file with shared configuration, then environment-specific files that import everything from the base and override what's needed.

This uses Python's `from module import *` syntax:

```python
# base.py - shared settings
SECRET_KEY = "shared-secret"
DEBUG = False

# local.py - development overrides
from .base import *
DEBUG = True  # Override for development
```

**Why this works**: The import statement brings all settings from `base.py` into `local.py`, then you selectively override specific values.

#### The 12-factor app methodology

From [12factor.net](https://12factor.net/config):

> **Factor III: Store config in the environment**
>
> An app's config is everything that is likely to vary between deploys (staging, production, developer environments). This includes:
>
> - Resource handles to databases, caches, and backing services
> - Credentials to external services
> - Per-deploy values such as the canonical hostname
>
> Apps sometimes store config as constants in code. This is a violation of twelve-factor, which requires strict separation of config from code.

**Key principle**: Configuration belongs in environment variables, not hardcoded in Python files. Django naturally supports this via `os.environ` or helper libraries like `django-environ`.

### Implementation steps

#### Step 1: Install django-environ

`django-environ` simplifies reading environment variables with type coercion and `.env` file support.

```bash
cd travelmathlite
uv add django-environ
```

**What django-environ provides**:

- **Type-safe parsing**: `env.bool('DEBUG')`, `env.int('PORT')`, `env.list('ALLOWED_HOSTS')`
- **URL parsing**: `env.db_url('DATABASE_URL')` parses `postgres://user:pass@host:5432/dbname`
- **`.env` file support**: Automatically reads local `.env` files for development convenience
- **Sensible defaults**: `env('KEY', default='fallback')`

#### Step 2: Create settings package structure

Convert the monolithic `settings.py` into a package:

```bash
cd travelmathlite/core
mkdir settings
touch settings/__init__.py
```

**Package initialization** (`travelmathlite/core/settings/__init__.py`):

```python
"""Settings package for travelmathlite.

Defaults to local settings for development convenience.
Override with DJANGO_SETTINGS_MODULE environment variable:
- DJANGO_SETTINGS_MODULE=core.settings.prod for production
- DJANGO_SETTINGS_MODULE=core.settings.local for development (default)
"""

from .local import *  # noqa: F401, F403
```

**Why default to local?**

- **Developer convenience**: Running `python manage.py runserver` works immediately without setting environment variables
- **Explicit production**: Production deployments must explicitly set `DJANGO_SETTINGS_MODULE=core.settings.prod`
- **Fail-safe design**: You can never accidentally use development settings in production (production must opt-in)

#### Step 3: Create base.py with shared configuration

**File**: `travelmathlite/core/settings/base.py`

```python
"""Base settings for the project.

Contains environment-driven defaults and shared configuration.
Uses django-environ to parse environment variables and support .env files.
"""

from pathlib import Path
import os
import environ

# Build paths inside the project
# base.py is at travelmathlite/core/settings/base.py
# Go three levels up to reach travelmathlite/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environ with type hints
env = environ.Env(
    DJANGO_DEBUG=(bool, False),  # Default to False for safety
)

# Read .env file if present (local development convenience)
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="change-me-local-dev")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "apps.calculators",
    "apps.airports",
    "apps.accounts",
    "apps.trips",
    "apps.search",
    "apps.base",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise for static files (configured in prod.py)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# Default to SQLite when DATABASE_URL not provided
DATABASE_URL = env("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {"default": env.db_url_config(DATABASE_URL)}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, images)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = Path(os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles"))

# Media files (user uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT", BASE_DIR / "media"))

# Manifest static files policy
USE_MANIFEST_STATIC = os.getenv("USE_MANIFEST_STATIC", "0").lower() in ("1", "true", "yes")

if not DEBUG or USE_MANIFEST_STATIC:
    STATICFILES_STORAGE = os.getenv(
        "STATICFILES_STORAGE",
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    )

# WhiteNoise cache duration (1 year default)
WHITENOISE_MAX_AGE = int(os.getenv("WHITENOISE_MAX_AGE", "31536000"))

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication redirects
LOGIN_REDIRECT_URL = "base:index"
LOGOUT_REDIRECT_URL = "base:index"

# Application-specific settings (calculator defaults)
ROUTE_FACTOR: float = float(os.getenv("ROUTE_FACTOR", "1.2"))
AVG_SPEED_KMH: float = float(os.getenv("AVG_SPEED_KMH", "80"))
FUEL_PRICE_PER_LITER: float = float(os.getenv("FUEL_PRICE_PER_LITER", "1.50"))
FUEL_ECONOMY_L_PER_100KM: float = float(os.getenv("FUEL_ECONOMY_L_PER_100KM", "7.5"))
```

**Key implementation details**:

1. **BASE_DIR calculation**: `parent.parent.parent` because `base.py` is nested three levels deep in `core/settings/`
2. **Type hints in Env()**: The constructor argument `DJANGO_DEBUG=(bool, False)` tells django-environ to parse as boolean with False as default
3. **Conditional .env loading**: Only loads if file exists (production won't have a `.env` file)
4. **env.list()**: Parses comma-separated strings into Python lists automatically
5. **env.db_url_config()**: Parses database URLs like `postgres://user:pass@host:5432/dbname` into Django's `DATABASES` dict format

#### Step 4: Create local.py for development

**File**: `travelmathlite/core/settings/local.py`

```python
"""Local development settings.

Inherits from base and enables DEBUG mode with developer-friendly defaults.
Use this for running `python manage.py runserver` locally.
"""

from .base import *  # noqa: F401, F403

# Enable debug mode for local development
DEBUG = True

# Allow all hosts in development (convenient for testing different hostnames)
ALLOWED_HOSTS = ["*"]

# Explicitly use SQLite for development (base.py already defaults to this)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Development-only apps (optional)
INSTALLED_APPS += [  # noqa: F405
    # Example: add django-debug-toolbar here
    # "debug_toolbar",
]

# Disable HTTPS/security features in development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Console email backend (prints to terminal instead of sending)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Development logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

**Development-specific features**:

- **DEBUG = True**: Shows detailed error pages, auto-reloads on code changes, shows template context
- **ALLOWED_HOSTS = ["*"]**: Accepts any hostname (localhost, 127.0.0.1, VM IP addresses, etc.)
- **Insecure cookies**: `SESSION_COOKIE_SECURE = False` allows cookies over HTTP
- **Console email**: Emails print to terminal instead of requiring an SMTP server

#### Step 5: Create prod.py for production

**File**: `travelmathlite/core/settings/prod.py`

```python
"""Production settings with security hardening.

Inherits from base and enforces secure defaults for production deployment.
Must be explicitly selected via DJANGO_SETTINGS_MODULE=core.settings.prod
"""

from .base import *  # noqa: F401, F403
import os

# SECURITY: Production must NEVER enable DEBUG
DEBUG = False

# SECURITY: SECRET_KEY is required in production (no default)
SECRET_KEY = env("SECRET_KEY")  # noqa: F405

# SECURITY: ALLOWED_HOSTS must be explicitly set
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

# HTTPS enforcement
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # noqa: F405
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# WhiteNoise compressed manifest storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Production logging (structured format)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL", default="INFO"),  # noqa: F405
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

# Database check: production must use proper database
if "DATABASE_URL" not in os.environ:
    raise ValueError("DATABASE_URL environment variable is required in production")
```

**Production security hardening**:

- **DEBUG = False**: Never show detailed error pages to users
- **Required environment variables**: `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL` have no defaults and will raise errors if missing
- **HTTPS enforcement**: All cookies marked `Secure`, HTTP redirects to HTTPS
- **HSTS (HTTP Strict Transport Security)**: Tells browsers to always use HTTPS for 1 year
- **Security headers**: Protects against clickjacking, MIME sniffing, XSS
- **WhiteNoise**: Compressed manifest storage for efficient static file serving

### Testing the settings split

#### Step 6: Verify settings modules import correctly

```bash
cd travelmathlite

# Test base.py
uv run python -c "import core.settings.base; print('✓ base.py OK')"

# Test local.py  
uv run python -c "import core.settings.local; print('✓ local.py OK')"

# Test prod.py (requires environment variables)
SECRET_KEY=test-key ALLOWED_HOSTS=example.com DATABASE_URL=sqlite:///test.db \
  uv run python -c "import core.settings.prod; print('✓ prod.py OK')"
```

**Expected output**:

```
✓ base.py OK
✓ local.py OK
✓ prod.py OK
```

#### Step 7: Verify Django recognizes the settings

```bash
# Default (uses core.settings.__init__ → core.settings.local)
uv run python manage.py check

# Explicitly use local
DJANGO_SETTINGS_MODULE=core.settings.local uv run python manage.py check

# Use prod (requires environment variables)
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test-key \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py check
```

**Expected output**:

```
System check identified no issues (0 silenced).
```

### Verification

**Verify DEBUG setting differs by environment**:

```bash
# Local (should be True)
uv run python manage.py shell -c "from django.conf import settings; print(f'DEBUG={settings.DEBUG}')"

# Prod (should be False)
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py shell -c "from django.conf import settings; print(f'DEBUG={settings.DEBUG}')"
```

**Expected output**:

```
DEBUG=True
DEBUG=False
```

---

## Section 2 — Environment variables and django-environ

**Brief**: `docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-02-environment-variables.md`

### Brief context and goal

Provide a `.env.example` file documenting all environment variables and create operations documentation showing how to configure the application for local development and production deployment.

### Relevant concepts

#### The .env file pattern

From the django-environ documentation:

> `.env` files provide a convenient way to set environment variables for local development. The file contains `KEY=value` pairs, one per line, and is read automatically when django-environ's `read_env()` is called.

**Best practices**:

- **Never commit `.env` to version control** (add to `.gitignore`)
- **Commit `.env.example`** with dummy/safe values as documentation  
- **Each developer has their own `.env`** with real values
- **Production uses real environment variables**, not `.env` files

#### Environment variable types in django-environ

From Matt Layman's "Understand Django":

> Environment variables are always strings, but your application needs different types. django-environ handles type conversion automatically with methods like `env.bool()`, `env.int()`, and `env.list()`.

**Type conversion methods**:

```python
env('VAR')                    # String (no conversion)
env.bool('VAR')               # Boolean: true/false, 1/0, yes/no, on/off
env.int('VAR')                # Integer
env.float('VAR')              # Float  
env.list('VAR')               # List from comma-separated values
env.dict('VAR')               # Dict from JSON string
env.url('VAR')                # URL parser
env.db_url('DATABASE_URL')    # Database URL parser
```

**Database URL format**:

```python
# PostgreSQL
DATABASE_URL=postgres://user:password@host:5432/dbname

# MySQL
DATABASE_URL=mysql://user:password@host:3306/dbname

# SQLite
DATABASE_URL=sqlite:///path/to/db.sqlite3
```

### Implementation steps

#### Step 1: Create .env.example

Create `travelmathlite/.env.example`:

```bash
# .env.example - Environment variable template
# Copy this file to .env and customize with your values
# NEVER commit .env to version control

# Django core settings
SECRET_KEY=change-me-to-a-random-50-character-string
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database configuration
# SQLite (default for development)
DATABASE_URL=sqlite:///db.sqlite3
# PostgreSQL example (production)
# DATABASE_URL=postgres://user:password@localhost:5432/travelmathlite

# Static and media files
STATIC_ROOT=staticfiles
MEDIA_ROOT=media
USE_MANIFEST_STATIC=0

# WhiteNoise configuration  
WHITENOISE_MAX_AGE=31536000

# Security settings (production only)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0

# Calculator defaults
ROUTE_FACTOR=1.2
AVG_SPEED_KMH=80
FUEL_PRICE_PER_LITER=1.50
FUEL_ECONOMY_L_PER_100KM=7.5

# Logging
LOG_LEVEL=INFO
```

**Why .env.example is important**:

- Documents all available configuration options
- Shows example/dummy values (safe to commit)
- Serves as a checklist for deployment
- Helps new developers get started quickly

#### Step 2: Add .env to .gitignore

Ensure `.env` is excluded from version control:

```bash
# .gitignore
.env
*.pyc
__pycache__/
db.sqlite3
/staticfiles/
/media/
.DS_Store
```

#### Step 3: Create .env for local development

```bash
cd travelmathlite
cp .env.example .env
```

Edit `.env` with your local values:

```bash
# .env - Local development configuration (DO NOT COMMIT)
SECRET_KEY=local-dev-secret-not-for-production-use
DJANGO_DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

#### Step 4: Create operations documentation

Create `docs/travelmathlite/ops/settings.md`:

```markdown
# Settings and Configuration

## Environment-based configuration

TravelMathLite uses environment variables for configuration, following the
[12-factor app methodology](https://12factor.net/config).

### Settings modules

- `core.settings.base` - Shared configuration for all environments
- `core.settings.local` - Development (DEBUG=True, permissive security)  
- `core.settings.prod` - Production (DEBUG=False, security hardening)

### Local development

1. Copy `.env.example` to `.env`:
   ```bash
   cd travelmathlite
   cp .env.example .env
   ```

2. Edit `.env` with your local values (customize SECRET_KEY, DATABASE_URL, etc.)

3. Run the development server:

   ```bash
   uv run python manage.py runserver
   ```

   The default `core.settings` imports from `core.settings.local`.

### Production deployment

1. Set environment variables (no `.env` file):

   ```bash
   export DJANGO_SETTINGS_MODULE=core.settings.prod
   export SECRET_KEY=<your-secret-key>
   export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   export DATABASE_URL=postgres://user:pass@host:5432/dbname
   ```

2. Collect static files:

   ```bash
   uv run python manage.py collectstatic --noinput
   ```

3. Run migrations:

   ```bash
   uv run python manage.py migrate
   ```

4. Start application server (gunicorn, uvicorn, etc.)

### Required environment variables

#### Development (local.py)

- `SECRET_KEY` - Django secret key (has safe default for dev)
- `DJANGO_DEBUG` - Boolean, defaults to True

#### Production (prod.py)  

- `SECRET_KEY` - REQUIRED (no default)
- `ALLOWED_HOSTS` - REQUIRED comma-separated list
- `DATABASE_URL` - REQUIRED database connection string
- `SECURE_SSL_REDIRECT` - Boolean, default True
- `SECURE_HSTS_SECONDS` - Integer, default 31536000

### Generating a SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### DATABASE_URL formats

```bash
# PostgreSQL
DATABASE_URL=postgres://user:password@host:5432/dbname

# MySQL  
DATABASE_URL=mysql://user:password@host:3306/dbname

# SQLite (development only)
DATABASE_URL=sqlite:///db.sqlite3
```

### Environment variable precedence

1. Real environment variables (highest priority)
2. `.env` file (local development convenience)
3. Defaults in settings files (lowest priority)

```

### Testing environment variable loading

#### Step 5: Test .env file reading

```bash
cd travelmathlite

# Create a test .env
echo "TEST_VAR=from-dotenv-file" > .env

# Verify django-environ reads it
uv run python -c "
import environ
env = environ.Env()
env.read_env('.env')
print(f'TEST_VAR={env(\"TEST_VAR\")}')
"
```

**Expected output**:

```
TEST_VAR=from-dotenv-file
```

#### Step 6: Test environment variable override

```bash
# Real environment variables override .env file
TEST_VAR=from-environment uv run python -c "
import os
print(f'TEST_VAR={os.getenv(\"TEST_VAR\")}')
"
```

**Expected output**:

```
TEST_VAR=from-environment
```

### Verification

**Verify SECRET_KEY is read from environment**:

```bash
cd travelmathlite
export SECRET_KEY=my-custom-test-secret

uv run python manage.py shell -c "
from django.conf import settings
print(f'SECRET_KEY={settings.SECRET_KEY}')
"
```

**Expected**: `SECRET_KEY=my-custom-test-secret`

---

## Section 3 — Production security and WhiteNoise

**Brief**: `docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-03-production-security.md`

### Brief context and goal

Enforce production security settings (HTTPS enforcement, secure cookies, HSTS headers) and integrate WhiteNoise for efficient static file serving without requiring nginx or a separate CDN.

### Relevant Django security concepts

#### HTTPS and secure cookies

From the Django security documentation:

> If a website allows HTTP connections and uses cookies for authentication, users' sessions can be stolen by anyone able to monitor the network. Django provides settings to enforce HTTPS and mark cookies as secure.

**HTTPS enforcement settings**:

- `SECURE_SSL_REDIRECT = True`: Redirects all HTTP requests to HTTPS
- `SESSION_COOKIE_SECURE = True`: Only send session cookie over HTTPS
- `CSRF_COOKIE_SECURE = True`: Only send CSRF token over HTTPS

**Why this matters**: Without these settings, cookies can be intercepted over unencrypted HTTP connections (man-in-the-middle attacks).

#### HTTP Strict Transport Security (HSTS)

From Mozilla Developer Network:

> HTTP Strict Transport Security (HSTS) is a web security policy mechanism that helps protect websites against protocol downgrade attacks and cookie hijacking. It allows web servers to declare that browsers should only interact with them using secure HTTPS connections.

**Django HSTS settings**:

- `SECURE_HSTS_SECONDS = 31536000`: Browsers remember preference for 1 year
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: Apply to all subdomains  
- `SECURE_HSTS_PRELOAD = True`: Eligible for browser preload lists

**Important**: Once HSTS is enabled, you cannot easily disable HTTPS without breaking your site for returning visitors (their browsers will refuse HTTP connections).

#### Security headers

**Additional protection headers**:

- `X_FRAME_OPTIONS = 'DENY'`: Prevents clickjacking by disallowing iframe embedding
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents browsers from MIME-type sniffing
- `SECURE_BROWSER_XSS_FILTER = True`: Enables browser XSS filtering (legacy)

#### WhiteNoise for static file serving

From the WhiteNoise documentation:

> WhiteNoise allows your web app to serve its own static files, making it a self-contained unit that can be deployed anywhere without relying on nginx, Amazon S3, or any other external service.

**Benefits**:

- Simplifies deployment (no separate static file server required)
- Automatic compression (gzip and Brotli)
- Optimal cache headers (`Cache-Control: public, max-age=31536000`)
- Works with Django's `ManifestStaticFilesStorage` for automatic cache-busting

**How it works**: WhiteNoise is a WSGI middleware that intercepts requests for static files and serves them directly from the `STATIC_ROOT` directory with optimal headers and compression.

### Implementation steps

#### Step 1: Install WhiteNoise

```bash
cd travelmathlite
uv add whitenoise
```

#### Step 2: Verify WhiteNoise middleware (already in base.py)

The middleware was added in Section 1:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Must be after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    # ... other middleware
]
```

**Middleware ordering is critical**:

1. `SecurityMiddleware` - Sets security headers first
2. `WhiteNoiseMiddleware` - Serves static files (must be early to intercept requests)
3. All other middleware

#### Step 3: Configure static file storage for production

In `prod.py`, WhiteNoise's compressed manifest storage is configured:

```python
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
```

**What this storage backend does**:

- Creates hashed filenames (`app.js` → `app.a1b2c3d4.js`)
- Generates `staticfiles.json` manifest mapping original names to hashed names
- Compresses files with gzip and Brotli
- Sets far-future cache headers (`max-age=31536000`)

#### Step 4: Test static file collection

```bash
cd travelmathlite

# Clear existing static files
rm -rf staticfiles

# Collect with production settings
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py collectstatic --noinput
```

**Expected output**:

```
X static files copied to '/path/to/staticfiles', Y post-processed.
```

**Verify manifest was created**:

```bash
ls staticfiles/staticfiles.json
cat staticfiles/staticfiles.json | head -20
```

You should see JSON mapping original filenames to their hashed versions.

### Testing security settings

#### Step 5: Verify security headers

Django provides a deployment checklist command:

```bash
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py check --deploy
```

**Expected output**:

```
System check identified no issues (0 silenced).
```

If issues are found, Django lists specific security warnings with recommended fixes.

#### Step 6: Test production invariants

```bash
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py shell -c "
from django.conf import settings

assert not settings.DEBUG, 'DEBUG must be False in production'
assert settings.SESSION_COOKIE_SECURE, 'Session cookies must be secure'
assert settings.CSRF_COOKIE_SECURE, 'CSRF cookies must be secure'  
assert settings.SECURE_HSTS_SECONDS > 0, 'HSTS must be enabled'

print('✓ All security checks passed')
"
```

### Verification

**Security checklist**:

- [ ] DEBUG is False
- [ ] SECRET_KEY is set from environment (not hardcoded)
- [ ] ALLOWED_HOSTS is explicitly set
- [ ] SESSION_COOKIE_SECURE is True
- [ ] CSRF_COOKIE_SECURE is True
- [ ] SECURE_SSL_REDIRECT is True
- [ ] SECURE_HSTS_SECONDS > 0
- [ ] WhiteNoise middleware is enabled
- [ ] Static files use compressed manifest storage

---

## Section 4 — Tests and invariants

**Brief**: `docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-04-tests-and-invariants.md`

### Brief context and goal

Create automated tests that verify settings behavior in different environments and document invariants (conditions that must always be true).

### Relevant testing concepts

#### Testing Django settings

From Django's testing documentation:

> Settings can be tested by importing the settings modules directly and checking their values. Use `unittest.mock.patch.dict` to temporarily set environment variables during tests.

**Testing strategies**:

1. **Import testing**: Import settings modules and assert values
2. **Override testing**: Use `@override_settings` to temporarily change settings
3. **Environment testing**: Mock `os.environ` to test environment variable handling

#### Settings invariants

An invariant is a condition that must always hold true. For Django settings:

**Local invariants**:

- DEBUG = True
- ALLOWED_HOSTS includes "*" or specific dev hostnames
- Secure cookie flags are False
- SQLite database

**Production invariants**:

- DEBUG = False (CRITICAL)
- SECRET_KEY set from environment (no default)
- ALLOWED_HOSTS explicitly set
- DATABASE_URL set
- Secure cookie flags are True
- HSTS enabled

### Implementation steps

#### Step 1: Create tests for local settings

Create `travelmathlite/core/tests/test_settings_local.py`:

```python
"""Tests for local (development) settings.

Verifies that local settings enable DEBUG and developer-friendly defaults.
"""

import os
from unittest.mock import patch
from django.test import SimpleTestCase, override_settings


class LocalSettingsTestCase(SimpleTestCase):
    """Test local settings configuration."""

    @override_settings(SETTINGS_MODULE="core.settings.local")
    def test_debug_enabled_in_local(self) -> None:
        """Test that DEBUG is True in local settings."""
        from django.conf import settings
        from importlib import reload
        import core.settings.local
        
        reload(core.settings.local)
        self.assertTrue(settings.DEBUG)

    def test_local_settings_import(self) -> None:
        """Test that local settings import without errors."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-key"}):
            import core.settings.local
            self.assertIsNotNone(core.settings.local)

    def test_local_allows_all_hosts(self) -> None:
        """Test that local settings accept any hostname."""
        from core.settings import local
        self.assertIn("*", local.ALLOWED_HOSTS)

    def test_local_uses_sqlite(self) -> None:
        """Test that local settings default to SQLite."""
        from core.settings import local
        self.assertEqual(
            local.DATABASES["default"]["ENGINE"],
            "django.db.backends.sqlite3"
        )

    def test_local_disables_secure_cookies(self) -> None:
        """Test that local settings disable secure cookie requirements."""
        from core.settings import local
        self.assertFalse(local.SESSION_COOKIE_SECURE)
        self.assertFalse(local.CSRF_COOKIE_SECURE)
        self.assertFalse(local.SECURE_SSL_REDIRECT)
```

#### Step 2: Create tests for production settings

Create `travelmathlite/core/tests/test_settings_prod.py`:

```python
"""Tests for production settings.

Verifies that production settings enforce security and require proper config.
"""

import os
from unittest.mock import patch
from django.test import SimpleTestCase


class ProductionSettingsTestCase(SimpleTestCase):
    """Test production settings configuration."""

    def test_prod_requires_secret_key(self) -> None:
        """Test that production requires SECRET_KEY environment variable."""
        with patch.dict(os.environ, {}, clear=False):
            if "SECRET_KEY" in os.environ:
                del os.environ["SECRET_KEY"]
            
            os.environ["ALLOWED_HOSTS"] = "example.com"
            os.environ["DATABASE_URL"] = "sqlite:///test.db"
            
            # Should raise when SECRET_KEY missing
            with self.assertRaises((KeyError, ValueError)):
                import core.settings.prod
                from importlib import reload
                reload(core.settings.prod)

    def test_prod_debug_disabled(self) -> None:
        """Test that DEBUG is False in production."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "ALLOWED_HOSTS": "example.com",
            "DATABASE_URL": "sqlite:///test.db"
        }):
            import core.settings.prod
            from importlib import reload
            reload(core.settings.prod)
            self.assertFalse(core.settings.prod.DEBUG)

    def test_prod_enables_secure_cookies(self) -> None:
        """Test that production enables secure cookie flags."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "ALLOWED_HOSTS": "example.com",
            "DATABASE_URL": "sqlite:///test.db"
        }):
            import core.settings.prod
            from importlib import reload
            reload(core.settings.prod)
            self.assertTrue(core.settings.prod.SESSION_COOKIE_SECURE)
            self.assertTrue(core.settings.prod.CSRF_COOKIE_SECURE)

    def test_prod_enables_hsts(self) -> None:
        """Test that production enables HSTS."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "ALLOWED_HOSTS": "example.com",
            "DATABASE_URL": "sqlite:///test.db"
        }):
            import core.settings.prod
            from importlib import reload
            reload(core.settings.prod)
            self.assertGreater(core.settings.prod.SECURE_HSTS_SECONDS, 0)
            self.assertTrue(core.settings.prod.SECURE_HSTS_INCLUDE_SUBDOMAINS)

    def test_prod_uses_whitenoise_storage(self) -> None:
        """Test that production uses WhiteNoise compressed storage."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "ALLOWED_HOSTS": "example.com",
            "DATABASE_URL": "sqlite:///test.db"
        }):
            import core.settings.prod
            from importlib import reload
            reload(core.settings.prod)
            self.assertIn(
                "whitenoise",
                core.settings.prod.STATICFILES_STORAGE.lower()
            )

    def test_prod_requires_database_url(self) -> None:
        """Test that production requires DATABASE_URL."""
        with patch.dict(os.environ, {
            "SECRET_KEY": "test-key",
            "ALLOWED_HOSTS": "example.com"
        }):
            # Missing DATABASE_URL should raise
            with self.assertRaises(ValueError):
                import core.settings.prod
                from importlib import reload
                reload(core.settings.prod)
```

**Testing strategy**:

- Uses `SimpleTestCase` (no database needed)
- Uses `unittest.mock.patch.dict` to set environment variables
- Uses `importlib.reload` to force re-import after changing environment
- Tests both positive cases (correct config) and negative cases (missing required vars)

#### Step 3: Run the tests

```bash
cd travelmathlite

# Run local settings tests
uv run python manage.py test core.tests.test_settings_local

# Run production settings tests  
uv run python manage.py test core.tests.test_settings_prod

# Run both together
uv run python manage.py test core.tests.test_settings_local core.tests.test_settings_prod
```

**Expected output**:

```
Found 11 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.023s

OK
Destroying test database for alias 'default'...
```

### Verification

**Run Django's deployment checklist**:

```bash
# Local (will show warnings - that's expected)
DJANGO_SETTINGS_MODULE=core.settings.local \
  uv run python manage.py check --deploy

# Production (should pass)
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py check --deploy
```

---

## Summary

This tutorial covered comprehensive environment-based configuration for Django:

### What we built

1. **Settings Package** (`core/settings/`)
   - `__init__.py` - Defaults to local
   - `base.py` - Shared configuration with django-environ
   - `local.py` - Development overrides
   - `prod.py` - Production hardening

2. **Environment Variables**
   - `django-environ` for type-safe parsing
   - `.env.example` documentation
   - `.env` file support for local dev
   - Production uses real environment variables

3. **Production Security**
   - HTTPS enforcement
   - Secure cookies
   - HSTS headers
   - Security headers (X-Frame-Options, etc.)
   - WhiteNoise for static files
   - Required environment variables

4. **Testing**
   - 5 tests for local settings
   - 6 tests for production settings
   - Environment variable mocking
   - Django deployment checklist integration

5. **Documentation** (`docs/travelmathlite/ops/settings.md`)
   - Environment usage
   - Required vs optional variables
   - DATABASE_URL formats
   - SECRET_KEY generation

### Key learning outcomes

- **Settings organization**: Environment-specific modules
- **12-factor methodology**: Config in environment
- **Type-safe configuration**: django-environ parsing
- **Security hardening**: HTTPS, HSTS, secure cookies
- **WhiteNoise**: Efficient static file serving
- **Testing**: Mocking environment variables
- **Invariants**: Conditions that must always be true

### Next steps

For production:

1. Use secrets manager (AWS Secrets Manager, Vault)
2. Automate migrations in deployment
3. Consider CDN for static files
4. Add monitoring and health checks
5. Implement database backup strategy
6. Use Let's Encrypt for SSL certificates

### References

- **ADR**: `docs/travelmathlite/adr/adr-1.0.8-settings-configuration-and-secrets.md`
- **Briefs**: `docs/travelmathlite/briefs/adr-1.0.8/`
- **Django settings**: <https://docs.djangoproject.com/en/5.2/topics/settings/>
- **Django deployment**: <https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/>
- **12-factor app**: <https://12factor.net/>
- **django-environ**: <https://django-environ.readthedocs.io/>
- **WhiteNoise**: <http://whitenoise.evans.io/>
- **Matt Layman "Understand Django"**: <https://www.mattlayman.com/understand-django/>

---

## Quick reference

```bash
# Local development
cd travelmathlite
cp .env.example .env  # First time
uv run python manage.py runserver

# Production deployment
export DJANGO_SETTINGS_MODULE=core.settings.prod
export SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
export ALLOWED_HOSTS=yourdomain.com
export DATABASE_URL=postgres://user:pass@host:5432/dbname
uv run python manage.py migrate
uv run python manage.py collectstatic --noinput

# Run tests
uv run python manage.py test core.tests.test_settings_local core.tests.test_settings_prod

# Check deployment readiness
DJANGO_SETTINGS_MODULE=core.settings.prod \
  SECRET_KEY=test \
  ALLOWED_HOSTS=example.com \
  DATABASE_URL=sqlite:///test.db \
  uv run python manage.py check --deploy
```
