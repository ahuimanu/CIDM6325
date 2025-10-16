# CIDM6325 - Fall 2025 #

README Outline:

- Matt Layman
  - [Chapter 1 - From Browser To Django](https://www.mattlayman.com/understand-django/browser-to-django/)
  - [Chapter 2 - URLs Lead The Way](https://www.mattlayman.com/understand-django/urls-lead-way/)
  - [Chapter 3 - Views On Views](https://www.mattlayman.com/understand-django/views-on-views/)
  - [Chapter 4 - Templates For User Interfaces](https://www.mattlayman.com/understand-django/templates-user-interfaces/)
  - [Chapter 5 - User Interaction With Forms](https://www.mattlayman.com/understand-django/user-interaction-forms/)
  - [Chapter 6 - Store Data With Models](https://www.mattlayman.com/understand-django/store-data-with-models/)
  - [Chapter 7 - Administer All The Things](https://www.mattlayman.com/understand-django/administer-all-the-things/)
  - [Chapter 8 - Anatomy Of An Application](https://www.mattlayman.com/understand-django/anatomy-of-an-application/)
  - [Chapter 9 - User Authentication](https://www.mattlayman.com/understand-django/user-authentication/)
  - [Chapter 10 - Middleware Do You Go?](https://www.mattlayman.com/understand-django/middleware-do-you-go/)
  - [Chapter 11 - Serving Static Files](https://www.mattlayman.com/understand-django/serving-static-files/)
  - [Chapter 12 - Test Your Apps](https://www.mattlayman.com/understand-django/test-your-apps/)
  - [Chapter 13 - Deploy A Site Live](https://www.mattlayman.com/understand-django/deploy-site-live/)
  - [Chapter 14 - Per-visitor Data With Sessions](https://www.mattlayman.com/understand-django/sessions/)
  - [Chapter 15 - Making Sense Of Settings](https://www.mattlayman.com/understand-django/settings/)
  - [Chapter 16 - User File Use](https://www.mattlayman.com/understand-django/media-files/)
  - [Chapter 17 - Command Your App](https://www.mattlayman.com/understand-django/command-apps/)
  - [Chapter 18 - Go Fast With Django](https://www.mattlayman.com/understand-django/go-fast/)
  - [Chapter 19 - Security And Django](https://www.mattlayman.com/understand-django/secure-apps/)
  - [Chapter 20 - Debugging Tips And Techniques](https://www.mattlayman.com/understand-django/debugging-tips-techniques/)

## Video and Chapter Notes ##

### Django Chapter 1: Django Basics ###

- URLs:
  - unlock web resources
  - provide the pathways into a static site as well as a dynamic web app
  - specify value and semantic paths
- Views:
  - Are the Python logic that "answers" when a URL ushers a visitor to it
    - [Views as Python functions](https://docs.djangoproject.com/en/5.2/topics/http/views/)
    - [Views as Python classes](https://docs.djangoproject.com/en/5.2/topics/class-based-views/)
      - [CBVs](https://ccbv.co.uk/)
      - Decorators and Mixins
  - Curate [responses](https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpResponse) to [requests](https://docs.djangoproject.com/en/5.2/ref/request-response/#django.http.HttpRequest)
- Django Templates:
  - Intersperse HTML markup and Data/Logic using [DTL](https://docs.djangoproject.com/en/5.2/topics/templates/).
  - Pass context (the data you want to use in the rendered page) from View to Template
  - Reuse with Template Inheritance
  - Use an [extensive toolkit](https://docs.djangoproject.com/en/5.2/ref/templates/builtins/) of helpers to extend template capabilities.
- Forms:
  - Use common HTML/HTTP structures to obtain user input
  - The form is both the HTML plus a Django class to maintain data/state about the form
  - Django helps with Form validation to ensure data consistency and safety.
- Models:
  - As a web application, Django's power is its assumption that we will use a database to store data rendered in pages.
  - Models represent data schema in the database (or any persistence store)
  - Models and the O/RM are how we save/read to/from the database.
  - Take care when you design/model your datases and entities.
- Videos:
  - Django 1: Django Basics
  - Django 2:
    - GitHub Repos, Copilot, and PRs
    - Copilot structures
    - Copilot Demo and Explanation

[back to outline](#cidm6325---fall-2025)

## Install & Packaging (pyproject.toml) ##

Treating this repo as a fresh workspace, here's a minimal `pyproject.toml` and step-by-step, copy-paste-ready commands to create an environment and install the project. The `pyproject.toml` below declares only Django 5.2.6 as the runtime dependency.

Minimal `pyproject.toml` (place at the repository root):

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "cidm6325"
version = "0.1.0"
description = "Minimal project declaring Django 5.2.6 as the sole dependency"
readme = "README.MD"
requires-python = ">=3.12"
authors = [{ name = "Your Name" }]
license = "MIT"
keywords = ["django"]
dependencies = [
  "Django==5.2.6"
]

[project.urls]
Homepage = "https://example.com/"
```

Commands (create venv, install build tools, install the project)

1. Create and activate a virtual environment

```bash
# make the venv
python -m venv .venv

# activate the venv

# on Windows: option 1
source .venv/Scripts/activate    # Git-Bash/WSL (bash)

# on Windows: option 2
# PowerShell: .\.venv\Scripts\Activate.ps1

# on Mac/*nix
# source ./.venv/bin/activate
```

1. Upgrade pip and install build helpers

```bash
python -m pip install --upgrade pip build
```

1. Install the local project (this will install Django 5.2.6 as declared)

```bash
python -m pip install .
# or editable/development mode
python -m pip install -e .
```

Verification

```bash
python -c "import django; print(django.get_version())"
# expected: 5.2.6
```

Quick troubleshooting

- If setuptools can't find packages to include when building, add package discovery (adjust if you use a `src/` layout):

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["yourpackagename*"]
# or for a src layout: where = ["src"]
```

- If you see a deprecation warning about `project.license` being a table, replace it with a short SPDX string, e.g. `license = "MIT"` (this README's example uses that form).
- To debug build-time failures, run `python -m build` and read the sdist/wheel output — it often shows missing metadata or packaging errors.
- If you want a pinned pip-style snapshot for CI, create it from an isolated env after installing: `pip freeze > requirements.txt`.

If you'd like, I can add a small GitHub Actions workflow that runs `python -m build` and verifies the Django version on push.

[back to outline](#cidm6325---fall-2025)

## Why this felt harder than `pip install -r requirements.txt` and troubleshooting ##

Short version: `requirements.txt` is just a list of packages for pip to install. `pyproject.toml` is a package manifest used by build tools (setuptools, wheel, etc.) and requires minimal package metadata (name, version) and sometimes package-discovery configuration so setuptools knows what to include in a wheel. That extra metadata is why you saw extra steps.

Quick checklist when migrating from `requirements.txt` to `pyproject.toml`:

- Make sure `pyproject.toml` lists your runtime dependencies under `[project].dependencies` (you have this).
- Tell setuptools how to find your packages if they live at the repo root (example already in this repo):

  [tool.setuptools.packages.find]
  where = ["."]
  include = ["blog*", "blogsite*"]

- Build and install using the venv Python to avoid mixing environments:

```bash
python -m venv .venv
source .venv/Scripts/activate    # on Git-Bash/WSL; on PowerShell use .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip build
python -m pip install .          # installs dependencies and your package
# or editable (dev) mode:
python -m pip install -e .
```

Common issues & quick fixes

- "setuptools couldn't find packages / set py_modules or packages": add a [tool.setuptools.packages.find] section with correct patterns (see example above). If your packages are under a `src/` directory, use `where = ["src"]`.
- Deprecation warnings about `project.license` as a TOML table: replace the table with an SPDX short string, e.g. `license = "MIT"` (done in this repo).
- If pip install fails during the build step, run `python -m build` to see the full build output and fix metadata errors.
- If you need a pip-style frozen file for CI, generate it from an isolated environment after install: `pip freeze > requirements.txt`.

If you'd like I can add a short GitHub Actions workflow that runs `python -m build` and `python -m pip install .` on push so the repo stays installable in CI.

## Docker Stuff ##

WSL2 is probably the best option for Windows.
![WSL2](./img/docker_install_dialog.png)

You can use the shell from within the Docker Interface
![Docker Interface](./img/docker_interface2.png)

Or, if on Windows, use PowerShell. If on Mac, Terminal is fine.
![PowerShell](./img/PowerShell.png)

`docker run --name=blog_db2 -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=xxxxx -p 5432:5432 -d postgres:latest`

steps:

1. `docker pull postgres` - I left the version off, so it gets the latest
2. `docker run --name=blog_db -e POSRGRES_DB=blog -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:latest` - note, you will realize the best results if you just stick to what Antonio is showing.
3. Although running `pip install psycopg` is a safe approach, it may not work entirely when doing a Docker container with Postgres, this mainly due to Postgres being virtualized where none of the resources used by Postgres are actually on your local system (Docker is). Your likely error message here will be "psycopg or psycopg2 not installed/found."
4. So, in case of issues with step 3 above, try this: `pip install "psycopg[binary]"` - this is recommended in the [psycopg documentation](https://www.psycopg.org/psycopg3/docs/basic/install.html#binary-installation).
5. Its also possible to rent a Postgres server from a number of places such as Digital Ocean.
6. The best way to see if all of this goes well is to run `python manage.py check` - this checks to see if Django will properly "bootstrap" itself to life. A good resposne is "System check identified no issues (0 silenced)."
7. `dumpdata` and `loaddata` may have failed depending on whether you followed the book exactly. Not a huge deal in development.
8. You can run/pause/stop the Postgres Docker container using the desktop application.

## Social Auth Notes ##

Clearly, the screens at the Developer Console for Google's Cloud Services are slightly different than the book.  However, the screens are similar.

Other notes:

1. It is CRITICAL that, in Windows, the hosts file is edited with a text editor that is started with evelated permissions  (right click and "Run as Administrator")
2. the Client ID from the "Client ID for Web Application" screen is the GOOGLE_OAUTH2_KEY
3. the Client secrete from from the "Client ID for Web Application" is the GOOGLE_OAUTH2_SECRET
4. django social auth is doing the rest of the "magic"

### Google Cloud ###

1. The URL for the overall cloud developer console is: [Google Cloud Console](https://console.cloud.google.com/)
2. A new project screen: ![New Project](./img/GC_new_project.png)
3. Select your project: ![Select Project](./img/GC_Select_Project.png)
4. Select OAuth Consent screen: ![Select OAUTH](./img/CG_Select_OAuth.png)
5. Enter App Info (name and Authorized Domains): ![Enter OAuth Info](./img/GC_App_Info.png)
6. Add Test User (must be the email you want to social auth with): ![Add Test User](./img/GC_Add_Test_User.png)
7. Create Credentials (dropdown shown and different from book): ![Select Credentials](./img/GC_Create_Credentials.png)
8. Create OAuth Cliend ID - Application Type "Web Application"; Add Authorized JavaScript Origings: Add Authorized redirect URIs: ![Client ID Settings](./img/GC_Client_ID_Settings.png)
9. Results Dialog - all info needed are on results diaglog: ![OAuth Dialog](./img/GC_OAuth_Client_Created.png)
10. Credentials Dashboard - ![OAuth Credentials Dashboard](./img/GC_Credentials_Dashboard.png)
11. Credentials Summary - ![OAuth Credentials Summary](./img/GC_Credials_Summary.png)

## RabbitMQ and Celery in Python ##

### RabbitMQ ###

RabbitMQ will run via Docker.  The commands in the book are straightforward:

1. Make sure Docker Desktop is running
2. grab the latest rabbitmq-management image: `docker pull rabbitmq:management`
3. run the image in a container: `docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management`

### Celery ###

1. On Windows, you will likely need to run a separate Git-Bash session with administrative rights (right-click and "Run as Administrator")
2. If not you will likely get this error `[WinError 5] Access Is Denied`, however, that is not the only source of this error on windows.

Let's look further into this:

1. For now, don't run Celery within VS Code (on windows) until I find a VS Code setting for you.
2. You WILL need to activiate the virtual environment in this new (separate) Git-Bash or PowerShell terminal
3. You will also want to limit the number of concurrent worker to something small for our testing purposes.  
4. Lastly, Windows has a hard time spawning new subprocesses and will utilizately thrlow the Access Denied error.
5. Although not mentioned in the book (because Antonio is likely developing on a Mac), we can use a Python "coroutine" trick using the [gevent](https://pypi.org/project/gevent/) package `pip install gevent` which utilizes greenlet to "fake" Python into using a single process as threads or coroutines. After installing `gevent` we can move on (as far as I can tell, this is Windows stuff).
6. So, try adjusting the command to the following: `celery -A myshop worker --loglevel=INFO --concurrency=4 -P gevent` and you should achieve success where the errors disappear.

You will be left with output that looks like the book, but the outlet is on the SEPARATE "Run As Admin" window.

``` shell
pip install gevent

celery -A myshop worker --loglevel=info -P gevent
```

In the end, sending an email via a message queue like celery and RabbitMQ is going to be a "nice to have" feature in the project.

## FINAL NOTE on the Blog ##

For all of the functions in the online shop example, it is expected that the following are always running:

1. Docker Desktop
2. RabbitMQ
3. Celery
4. A proper Stripe API connection

The shop won't run without these.  I know these external dependencies are a pain, but they represent a very realistic scenario for you to understand.

## MOre Docker Stuff ##

I don't specify a version of memchached, so it defaults to `latest`:

`docker pull memcached` - defaults to ***latest***

`docker run -it --rm --name memcached -p 11211:11211 memcached:latest -m 64`

Also for ***redis***:

`docker run -it --rm --name redis -p 6379:6379 redis:latest`

## General Notes ##

- DO NOT SKIP READING THE BOOK! As it is Free, [Matt Layman's Book](https://www.mattlayman.com/understand-django/browser-to-django/) is a little sparse, but it has the concepts we need.
- [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator) - you need this because the default secret key is not meant for deployment.
- Commands to run when checking for outdated packages in your Virtual Environment (VE):
  - Be sure that your VE is activated (`source .venv/Scripts/activate`)
  - check for outdated packages `python -m pip --outdated`
  - update package(s) as appropriate `python -m pip install --upgrade <name-of-package>`
- In addition to the book, this is a good resource: [W3Schools Django](https://www.w3schools.com/django/index.php)
- A [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/) is available as a quick reference for common `git` commands.
- Boostrap Crash Course (freecodecamp): [Full Bootstrap 5 Tutorial for Beginners](https://www.freecodecamp.org/news/full-bootstrap-5-tutorial-for-beginners/)

[back to outline](#cidm6325---fall-2025)

## Miscellaneous Notes ##

- **Templates and Bootstrap** - I will strongly recommend that you use and develop familiarity with [Bootstrap](https://getbootstrap.com/) as a CSS framework for all of your work in this class.
- **Classy Class-Based Views** - Should you wish to go in this direction: [https://ccbv.co.uk/](https://ccbv.co.uk/)
- **Environment Variables** - I have used [python-dotenv](https://pypi.org/project/python-dotenv/) forever and have done so in my code./
- **Candidate Heroku Replacements** - Heroku used to be the best free Django deployment platform - it is no longer free.  Here are some replacement services.
  - render.io
  - python anywhere
  - Fly.io
  - [Railway](https://railway.app/)

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

[back to outline](#cidm6325---fall-2025)

This will be a conflict with the FALL2024 branch.
