# CIDM6325 - Fall 2024
README Outline:

- A [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/) is available as a quick reference for common `git` commands.

# Professional Django Skills vs Book Order

[Pro Django Skills topics](https://www.better-simple.com/django/2023/08/18/pro-djangonaut-skills/) come from the [BetterSimple](https://www.better-simple.com/portfolio/) website.

Book Topic                      | Pro Django Skills Topic
---                             | ---
***Chapter 1***                 | ***Dev tools***
Django Project Structure        | [Git](https://training.github.com/downloads/github-git-cheat-sheet/) and [GitHub](https://docs.github.com/en/get-started)  
`django-admin` CLI              | [Black](https://pypi.org/project/black/), [PEP8](https://pep8.org/), [Flake8](https://pypi.org/project/flake8/)
Basic Views and URLs            | [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
Basic Templates                 | [Django Extensions](https://pypi.org/project/django-extensions/)
&nbsp;                          | [Awesome Django](https://awesomedjango.org/)
***Chapter 2***                 | ***Data modeling and Database***
Basic Database Concepts         | [Databases and RDBMS](https://database.guide/what-is-a-database/)
CRUD in SQL and ORM             | [DDL and DML in SQL](https://database.guide/sql-tutorial-for-beginners/)
Django ORM                      | [Relationships (1:1, 1:M, M:M)](https://database.guide/database-relationships-explained/)
Models and Migrations           | [Foreign Keys and Joins](https://database.guide/sql-joins-tutorial/)
Django ModelManagers            | [Normalization and Denormalization](https://database.guide/what-is-normalization/)
Q objects and queries           | [SQL Data Types](https://database.guide/database-tutorial-part-1-about-databases-creating-databases-tables/)
bulk_create and fixtures        | &nbsp;
&nbsp;                          | ***Django ORM***
&nbsp;                          | [Select related](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-related)
&nbsp;                          | [Prefetch related](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#prefetch-related)
&nbsp;                          | [Annotations](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.annotate)
&nbsp;                          | [Subqueries](https://docs.djangoproject.com/en/4.2/ref/models/expressions/#subquery-expressions)
&nbsp;                          | [Update or create](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#update-or-create)
&nbsp;                          | [bulk_create](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create)
&nbsp;                          | [bulk_update](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-update)
&nbsp;                          | [atomic transactions](https://docs.djangoproject.com/en/4.2/topics/db/transactions/#django.db.transaction.atomic)
&nbsp;                          | [select for update](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-for-update)
&nbsp;                          | [The Query Expression API](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-for-update)
***Chapter 3 and 11***          | ***Templates, Views and URLs***
Function-based views            | [Template inheritance](https://docs.djangoproject.com/en/4.2/ref/templates/language/#template-inheritance)
Class-based views               | [Includes](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#include)
ULR configuration               | [Template tags and filters](https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#)
Django templates and language   | &nbsp;
Django template language        | &nbsp;
Template filters                | &nbsp;
Custom template filters         | &nbsp;
string filters                  | &nbsp;
template tags                   | &nbsp;
***Chapter 4 and 10***          | ***Django Admin***
Superuser/admin account         | &nbsp;
CRUD in admin                   | &nbsp;
User management                 | &nbsp;
Model registration              | &nbsp;
Admin customization             | &nbsp;         
Adding new admin views          | &nbsp;
***Chapter 5***                 | ***Files Deployment***
Serving Static Files            | [Static files](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/)
`collectstatic` command         | [Media files](https://docs.djangoproject.com/en/4.2/topics/files/)
STATICFILES_FINDERS             | [Whitenoise](https://whitenoise.readthedocs.io/en/latest/)
static URLs                     | &nbsp;
STATICFILES_DIRS                | &nbsp;
`findstatic` command            | &nbsp;
***Chapter 6 and 7***           | ***Forms***
Forms and HTTP POST             | [Form vs ModelForm](https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/)
Django Forms Library            | [Custon - Server Side - Validation](https://docs.djangoproject.com/en/4.2/ref/forms/validation/)
Form validation                 | [Creating Custom Form Templates](https://docs.djangoproject.com/en/4.2/ref/forms/renderers/#overriding-built-in-form-templates)
Custom Form Field Validation    | [Django Crispy Forms](https://github.com/django-crispy-forms/django-crispy-forms)
Placeholders and initial values | [Formsets - Multi-part forms](https://docs.djangoproject.com/en/4.2/topics/forms/formsets/)
ModelForm                       | &nbsp;
***Chapter 8***                 | ***Forms***
File Uploads                    | [File Uploads](https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/)
Image Uploads                   | [Upload Handlers](https://docs.djangoproject.com/en/4.2/ref/files/uploads/)
ModelForms and Uploads          | [Images](https://djangocentral.com/uploading-images-with-django/)
***Chapter 9***                 | ***Sessions and Authorization***
Middleware                      | [Sessions](https://docs.djangoproject.com/en/4.2/topics/http/sessions/)
Password Handling               | [Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
Authentication decorators       | [Middleware](https://docs.djangoproject.com/en/4.2/topics/http/middleware/)
Template enhancements           | [CSRF](https://docs.djangoproject.com/en/4.2/ref/csrf/)
Sessions                        | [Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
&nbsp;                          | [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
&nbsp;                          | [HTTP Session](https://developer.mozilla.org/en-US/docs/Web/HTTP/Session)
&nbsp;                          | [Lifecycle of a HTTP request](https://firefox-source-docs.mozilla.org/networking/http/lifecycle.html)
&nbsp;                          | [Authentication and Authorization](https://docs.djangoproject.com/en/4.2/topics/auth/)
&nbsp;                          | [Granting permissions](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization)
&nbsp;                          | [Managing Groups](https://docs.djangoproject.com/en/4.2/topics/auth/default/#groups)
&nbsp;                          | [Django Single Signon - CAS](https://djangocas.dev/)
&nbsp;                          | [Custom Authentication Backend](https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-an-authentication-backend)
***Chapter 12***                | ***Django REST Framework for APIs***
Understanding REST APIs         | [Respresentational State Transfer](https://www.service-architecture.com/articles/web-services/representational-state-transfer-rest.html)
Serliaizers                     | [Rest Tutorial](https://www.restapitutorial.com/)
ViewSets                        | [JavaScript fetch method](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
&nbsp;                          | [HTMX](https://htmx.org/)
&nbsp;                          | [GraphQL](https://htmx.org/)
&nbsp;                          | [OAuth - authentication as a service](https://oauth.net/2/)
***Chapter 13***                | ***File Output Generation - PDF, CSV, Excel, graphs, etc.***
Working with CSV files          | [How to create CSV output](https://docs.djangoproject.com/en/4.2/howto/outputting-csv/)
Working with PDF files          | [how to create PDF files](https://docs.djangoproject.com/en/4.2/howto/outputting-pdf/)
Working with Excel files        | [Django and Excel](https://pypi.org/project/django-excel/)
Working with graphs             | [mathplotlib](https://matplotlib.org/)
Integrating visualizations      | &nbsp;
***Chapter 14***                | ***Testing Django and Python***
Testing fundamentals            | [Data setup - fixture loading](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#fixture-loading)
Automated testing               | [Testing in Django](https://docs.djangoproject.com/en/4.2/topics/testing/)
Testing in Django               | [Unit Test vs. Integration Test](https://www.testim.io/blog/unit-test-vs-integration-test/)
Testing Django models           | [Test-Driven Development](https://www.obeythetestinggoat.com/)
Testing Django views            | [Django Test Coverage](https://docs.djangoproject.com/en/4.2/topics/testing/advanced/#integration-with-coverage-py)
Django RequestFactory           | [Request Factory](https://docs.djangoproject.com/en/4.2/topics/testing/advanced/#the-request-factory)
Testcase Classes                | [Test automation with `tox`](https://tox.wiki/en/4.9.0/)
***Chapter 15***                | ***Django Third Party Libraries***
Finding 3rd party               | [Awesome Django](https://awesomedjango.org/)
Environment variables           | [Python Dotenv](https://pypi.org/project/python-dotenv/)
Django configurations           | [Django configurations](https://pypi.org/project/django-configurations/)
Handing database connections    | [DJ Database URL](https://pypi.org/project/dj-database-url/)
Django Debug Toolbar            | [Django Debug Toolbar](https://pypi.org/project/django-debug-toolbar/)
Django Crispy Forms             | [Django Crispy Forms](https://pypi.org/project/django-crispy-forms/)
Django Allauth                  | [Django Allauth](https://pypi.org/project/django-allauth/)
***Chapter 16***                | ***JavaScript Frontends***
ReactJS                         | [ReactJS](https://legacy.reactjs.org/docs/getting-started.html)
HTMX                            | [HTMX](https://htmx.org/) - I prefer this
AlpineJS                        | [AlpineJS](https://alpinejs.dev/) - "lighter" than ReactJS
jQuery                          | [jQuery](https://jquery.com/) - old and unfairly unpopular

**General Notes**
* [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator)

* Commands to run when checking for outdated packages in your Virtual Environment
    * Be sure that your VE is activated (`source .venv/Scripts/activate`)
    * check for outdated packages `python -m pip --outdated`
    * update package(s) as appropriate `python -m pip install --upgrade <name-of-package>`

In addition to the book, this is a good resource: [W3Schools Django](https://www.w3schools.com/django/index.php)

[back to outline](#cidm6325---fall-2024)

# Miscellaneous Notes
* **Templates and Bootstrap** - I will strongly recommend that you use and develop familiarity with [Bootstrap](https://getbootstrap.com/) as a CSS framework for all of your work in this class.
* **Candidate Heroku Replacements** - Heroku used to be the best free Django deployment platform - it is no longer free.  Here are some replacement services.
    * render.io
    * python anywhere
    * Fly.io
    * [Railway](https://railway.app/)

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

[back to outline](#cidm6325---fall-2024)
