# CIDM6325 - Fall 2023
README Outline:
* [Professional Django Skills vs Book Order](#professional-django-skills-vs-book-order) 
* [An Introduction to Django (Chapter 1)](#an-introduction-to-django-chapter-1)
* [Miscellaneous Notes](#miscellaneous-notes)

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
Testing fundamentals            | [Awesome Django](https://awesomedjango.org/)



[back to outline](#cidm6325---fall-2023)

**General Notes**
* [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator)

* Commands to run when checking for outdated packages in your Virtual Environment
    * Be sure that your VE is activated (`source .venv/Scripts/activate`)
    * check for outdated packages `python -m pip --outdated`
    * update package(s) as appropriate `python -m pip install --upgrade <name-of-package>`

In addition to the book, this is a good resource: [W3Schools Django](https://www.w3schools.com/django/index.php)

# An Introduction to Django (Chapter 1)
* Django is a web application framework that leverages the Python programming language.
* Django Features:
    * Object-Relational Mapper for database querying
    * URL mapping
    * template rendering 

Key learning objectives:
* project scaffolding with the `django-admin` CLI tool and the `manage.py` script
* MVC (MVT) application pattern paradigm
* Default Django project structure and apps
* Views for logic and template renders
* URL mapping to match requests to views
* Detecting and using HTTP Requests
    * [GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) and [POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) [Django](https://www.djangoproject.com/) [QueryDict](https://docs.djangoproject.com/en/4.2/ref/request-response/#querydict-objects) objects to obtain HTTP request parameter values
* How to configure your project in `settings.py` and check settings using `django.conf`
* Using HTML templates
* Working with Django errors and debugging

Try Activities:
* 1.01
* 1.02

[back to outline](#cidm6325---fall-2023)

# Models and Migrations (Chapter 2)
* SQLite is the default RDBMS system used by Django, it is a very capable solution, but also does not compare to something like [MySQL](https://www.mysql.com/) or [PostgreSQL](https://www.postgresql.org/). PostgreSQL is more preferred for many Django projects.
* The tool recommended in the chapter [DB Browser for SQLite](https://sqlitebrowser.org/) is very handy to get an understanding of what the DjangoORM is doing behind the scenes when the DjangoORM creates and executes SQL statements in the background.
* The Structured Query Language makes it possible to express a number of commands and intents to the RDBMS you are using, the book refers to the essential operations as CRUD (Create, Read, Update, and Delete), these are mostly [DQL/DML](https://www.geeksforgeeks.org/sql-ddl-dql-dml-dcl-tcl-commands/#) statements.
* The material in the book on using SQL is good for your reference, but we will mostly rely on the [DjangoORM](https://docs.djangoproject.com/en/4.2/#the-model-layer).
* However, it is possible to execute [Raw SQL](https://docs.djangoproject.com/en/4.2/topics/db/sql/) against a database via the DjangoORM.
* In nearly all cases, when starting out, SQLite will be sufficient - remember that SQLite creates a database file in your project.
* Databases, like most things, are governed by entries in the `settings.py` file used to [configure your Django project and apps](https://docs.djangoproject.com/en/4.2/topics/settings/).
* There is a tight integration between the apps you declare in `settings.py` and how the DjangoORM looks for and manages the database, the models declared in your app's `models.py` file are detected due to identifying your apps in `settings.py`.
* Migrations are important as the prime translation between the models you specify and the SQL that is written for communication with the underlying database.
* Although they are rooted in database fundamentals of relational models, getting the hang of [relationships](https://docs.djangoproject.com/en/4.2/topics/db/models/#relationships) in the DjagoORM and the models you create will take practice.
* Keep in mind that the purpose of an ORM is allow you to only work with in-memory objects in your code without having to deal with the particulars of SQL. Most of the chapter emphasizes this point.
* Q objects will seem odd at first, but they exist to facilitate complex queries that would require intermediate to advanced SQL techniques.
* Don't skip the exercises in this chapter, they will help and the authors have provided solutions.

## Observations
Object/Relational Mappers are among the more poignant and impactful developments along the way to writing web applications.  In most cases, any software's true efficacy is to apply logic and business rules to both incoming and outgoing data.  It can be said that it is the application of these rules that creates the value that allows the elevation of data to information.  Some understanding of the fundamentals of databases and database design is a helpful pre-requisite to working with this information.  I commend the authors (and I am grateful to them for writing a useful book) for providing some basic treatment. 

Do this activity:
* 2.01

[back to outline](#cidm6325---fall-2023)

# URLs, Views, and Templates (Chapter 3)
* Views are language derived from a application design pattern called the [Model View Controller](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). However, in Django, this is commonly referred to as Model View Template. The discintions are too important
* What is generally happening is that we need a way to translate an incoming URL request to represent a specified request of the Django applicaiton and then render the correct response
* This is all pursuant to the [HTTP request cycle](https://developer.mozilla.org/en-US/docs/Web/HTTP/Session) (usually a GET followed by a response).
* The common approach is to create an app-level `urls.py` file that integrates with a project-level `urls.py` file.  The purpose of this file is to map incoming URL patterns to the Python/Django code that will do something about the incoming request.
* This is the essence of a web application.
* Views represent the connection between an incoming URL-driven request and the response you will use accommodate that request.  Views will mediate and moderate that transaction.
* The two common approaches to this are function-based views and class-based views.
* Both generally make it possible to receive an [HTTP Request object](https://docs.djangoproject.com/en/4.2/topics/http/) and handle any [response](https://docs.djangoproject.com/en/4.2/ref/request-response/), which is typically rendered HTML.
* The entire purpose of a template is to intersperse and combine HTML/CSS markup with Python/Django code that directs either logic or data - sometimes both.
* For this reason, there is a Django Template Language available to us, but it not so much a language, but a method for combining the HTML/CSS, code, and data needed to create the "Web" part of the web application.
* Template inheritance and includes are very handy as they facilitate reuse by providing "chunks" and parts to reusbaly structure the pages delivered in HTML responses.
* I concur with the authors' approach to include Bootrstrap as a CSS/presentation framework as a part of your templates.  You will not likely win a design award with Bootstrap, but you will have a functional and highly-tested approach to creating very usable and presentable pages in your web application.
* I also strongly recommend the exercises in this chapter.

[back to outline](#cidm6325---fall-2023)

# Django Admin (Chapter 4 and 10)
* The Django admin is a secret weapon that many frameworks don't quite have - Perhaps CMSs like WordPress are an exception.
* Basically, you use the Django admin to manage the models and data in your application.
* The Django admin is a full web application within a web application designed to permit privileged access for the purposes of managing data in your project and its apps.
* The Django admin affords the opportunity to effect CRUD operations but is only admin focused and does not substitute for user-facing interfaces.
* The nice thing about the admin is that you can place a few test records into the databse and then use the `manage.py` or `django-admin` tools to export that data.  
* You can then import this data whenever you need to reset the project/application.
* The Django admin is also designed to manage users/groups and permissions (authentication and authorization).
* Registering your models for admin use is an explicit act specified by including an `admin.py` file in your app.
* You can also customize how the admin works with your models using and extending the [ModelAdmin](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin) class.
* Django admin interface customization is also possible via the [AdminSite](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#adminsite-objects) class.
* The Django admin is implemented as an available app that comes with a default scaffolded Django project.
* You can override the properties and behaviors of the default `AdminSite` object (that is available as long as the `admin` app is registered, which it is by default) in `settings.py`
* You can also customize the built-in adminsite templates to adjust other aspects of presentation and look-and-feel.
* AdminSite customization can be extended to adding/modifying the views that ship with the admin app.
* As ever, the exercises in chapter 4 are worth trying out.

# Static Files (Chapter 5 and 11)
* It is important to remember that Django is a web application framework and not an HTTP server.  
* Django is meant to work with an HTTP server in most cases, but Django also makes it easier to test your apps through its built-in webserver.
* In all cases, most web applications rely on static files, particularly CSS and JS files.
* Apps are ideally independent of each other, so a system of allowing static files to be located within an app, and yet made widely available once your project is deployed is why the `manage.py collectstatic` command exists.


[back to outline](#cidm6325---fall-2023)

# Miscellaneous Notes
* **Templates and Bootstrap** - I will strongly recommend that you use and develop familiarity with [Bootstrap](https://getbootstrap.com/) as a CSS framework for all of your work in this class.
* **Candidate Heroku Replacements** - Heroku used to be the best free Django deployment platform - it is no longer free.  Here are some replacement services.
    * render.io
    * python anywhere
    * Fly.io
    * [Railway](https://railway.app/)

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

[back to outline](#cidm6325---fall-2023)
