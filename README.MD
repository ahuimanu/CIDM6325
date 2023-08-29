# CIDM6325 - Fall 2023
README Outline:
* [Professional Django Skills vs Book Order](#professional-django-skills-vs-book-order) 
* [An Introduction to Django (Chapter 1)](#an-introduction-to-django-chapter-1)
* [Miscellaneous Notes](#miscellaneous-notes)

# Professional Django Skills vs Book Order

[Pro Django Skills topics](https://www.better-simple.com/django/2023/08/18/pro-djangonaut-skills/) come from the [BetterSimple](https://www.better-simple.com/portfolio/) website.

Book Topic                  | Pro Django Skills Topic
---                         | ---
***Chapter 1***             | ***Dev tools***
Django Project Structure    | [Git](https://training.github.com/downloads/github-git-cheat-sheet/) and [GitHub](https://docs.github.com/en/get-started)  
`django-admin` CLI          | [Black](https://pypi.org/project/black/), [PEP8](https://pep8.org/), [Flake8](https://pypi.org/project/flake8/)
Basic Views and URLs        | [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/)
Basic Templates             | [Django Extensions](https://pypi.org/project/django-extensions/)
&nbsp;                      | [Awesome Django](https://awesomedjango.org/)
***Chapter 2***             | ***Data modeling and Database***
Basic Database Concepts     | [Databases and RDBMS](https://database.guide/what-is-a-database/)
CRUD in SQL and ORM         | [DDL and DML in SQL](https://database.guide/sql-tutorial-for-beginners/)
Django ORM                  | [Relationships (1:1, 1:M, M:M)](https://database.guide/database-relationships-explained/)
Models and Migrations       | [Foreign Keys and Joins](https://database.guide/sql-joins-tutorial/)
Django ModelManagers        | [Normalization and Denormalization](https://database.guide/what-is-normalization/)
Q objects and queries       | [SQL Data Types](https://database.guide/database-tutorial-part-1-about-databases-creating-databases-tables/)
bulk_create and fixtures    | &nbsp;
&nbsp;                      | ***Data modeling and Database***
&nbsp;                      | [Select related](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#select-related)
&nbsp;                      | [Prefetch related](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#prefetch-related)
&nbsp;                      | [Annotations](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#django.db.models.query.QuerySet.annotate)
&nbsp;                      | [Subqueries](https://docs.djangoproject.com/en/4.2/ref/models/expressions/#subquery-expressions)
&nbsp;                      | [Update or create](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#update-or-create)
&nbsp;                      | [bulk_create](https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create)
***Chapter 3***             | ***Templates, Views and URLs***
Basic Database Concepts     | [Databases and RDBMS](https://database.guide/what-is-a-database/)



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

# Miscellaneous Notes
* **Templates and Bootstrap** - I will strongly recommend that you use and develop familiarity with [Bootstrap](https://getbootstrap.com/) as a CSS framework for all of your work in this class.
* **Candidate Heroku Replacements** - Heroku used to be the best free Django deployment platform - it is no longer free.  Here are some replacement services.
    * render.io
    * python anywhere
    * Fly.io
    * [Railway](https://railway.app/)

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

[back to outline](#cidm6325---fall-2023)
