# Code Repository for CIDM6325

Working with Django for web application and eCommerce development.

- [Code Repository for CIDM6325](#code-repository-for-cidm6325)
  * [Fall 2020](#fall-2020)
  * [Guide to Book Topics for Final Project (Baseline, Good, Better, Best)](#guide-to-book-topics-for-final-project--baseline--good--better--best-)
  * [EXTRAS](#extras)
  * [Python Tips and Guidance](#python-tips-and-guidance)
  * [Build a Blog Notes](#build-a-blog-notes)
  * [Chapter 1 - Build a Blog](#chapter-1---build-a-blog)
    + [Models](#models)
    + [Admin](#admin)
    + [Queries](#queries)
    + [Views](#views)
    + [Secret Key](#secret-key)
    + [Templates](#templates)
  * [Chapter 2 - Enhancing Your Blog with Advanced Features](#chapter-2---enhancing-your-blog-with-advanced-features)
    + [Forms and Email](#forms-and-email)
    + [Comments and Tags](#comments-and-tags)
  * [Chapter 3 - Extending the Blog Application](#chapter-3---extending-the-blog-application)
- [Bookmarks Social Site](#bookmarks-social-site)
  * [Chapter 4 - Bookmarks](#chapter-4---bookmarks)
  * [Chapter 5 - Images](#chapter-5---images)
    + [Many to Many Relationships](#many-to-many-relationships)
    + [Form Validation](#form-validation)
    + [The necessity of client-side code](#the-necessity-of-client-side-code)
    + [thumbnails](#thumbnails)
    + [AJAX](#ajax)
    + [Cross-Site Request Forgery](#cross-site-request-forgery)
    + [Custom View Decorators](#custom-view-decorators)
    + [Adding AJAX Pagination](#adding-ajax-pagination)
  * [Chapter 6 - Follow and Tracking](#chapter-6---follow-and-tracking)
    + [Building the Follow System](#building-the-follow-system)
    + [Building the Activity Stream](#building-the-activity-stream)
    + [Denormalization](#denormalization)
    + [App configuration](#app-configuration)
    + [REDIS for in-memory database function](#redis-for-in-memory-database-function)
- [Windows Subsystem for Linux](#windows-subsystem-for-linux)
  * [Working with VS Code](#working-with-vs-code)
  * [Mac or Linux](#mac-or-linux)
- [Online Shop](#online-shop)
  * [Chapter 7 - Creating an Online Shop Project](#chapter-7---creating-an-online-shop-project)
    + [Product Catalog](#product-catalog)
    + [Shopping Cart and Django Sessions](#shopping-cart-and-django-sessions)
      - [Django Sessions as Middleware](#django-sessions-as-middleware)
      - [Django Sessions Settings](#django-sessions-settings)
      - [Related Settings](#related-settings)
      - [Serialization](#serialization)
      - [Context Processors](#context-processors)
    + [Registering customer orders](#registering-customer-orders)
      - [Creating a Customer Order](#creating-a-customer-order)
    + [Launching asynchronous tasks with Celery](#launching-asynchronous-tasks-with-celery)
    + [Celery Installation](#celery-installation)
      - [RabbitMQ](#rabbitmq)
      - [Celery and Django](#celery-and-django)
      - [EMAIL BACKEND](#email-backend)
    + [Monitoring Celery](#monitoring-celery)
  * [Chapter 8 - Managing Payments and Orders](#chapter-8---managing-payments-and-orders)
    + [Payment Gateways](#payment-gateways)
      - [Braintree Sandbox Account](#braintree-sandbox-account)
      - [Braintree Python Integration](#braintree-python-integration)
    + [Integrating the payment gateway](#integrating-the-payment-gateway)
      - [Integrating Braintree using Hosted Fields](#integrating-braintree-using-hosted-fields)
    + [Exporting orders to CSV files](#exporting-orders-to-csv-files)
      - [Custom Admin Action](#custom-admin-action)
    + [Extending the administration site with custom views](#extending-the-administration-site-with-custom-views)
    + [Generating PDF invoices dynamically](#generating-pdf-invoices-dynamically)
  * [Chapter 9 - Coupons, Discounts, and Internationalization](#chapter-9---coupons--discounts--and-internationalization)
    + [Internationalization (i18n) and Localization (l10n)](#internationalization--i18n--and-localization--l10n-)
      - [Django Support for i18n and l10n](#django-support-for-i18n-and-l10n)
    + [Enabling i18n](#enabling-i18n)
    + [Recommender System](#recommender-system)
- [E-Learning Platform](#e-learning-platform)
  * [Chapter 10 - Building an E-Learning Platform](#chapter-10---building-an-e-learning-platform)
    + [Fixtures](#fixtures)
    + [Model Inheritance](#model-inheritance)
      - [Abstract Models](#abstract-models)
      - [Multi-table model inheritance](#multi-table-model-inheritance)
      - [Proxy models](#proxy-models)
    + [Creating custom model fields](#creating-custom-model-fields)
    + [Creating a CMS](#creating-a-cms)
    + [Managing course modules and their contents](#managing-course-modules-and-their-contents)
  * [Chapter 11 - Rendering and Caching](#chapter-11---rendering-and-caching)
  * [Chapter 12 - Django REST Framework](#chapter-12---django-rest-framework)
  * [Chapter 13 - Channels and ASGI](#chapter-13---channels-and-asgi)
- [Deployment - Antonio's Strategy and Mine](#deployment---antonio-s-strategy-and-mine)
  * [Chapter 14 - Deployment](#chapter-14---deployment)
  * [Managing settings](#managing-settings)
    + [uWSGI vs Gunicorn](#uwsgi-vs-gunicorn)
    + [nginx](#nginx)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Fall 2020

We will work through Antonio Melé's [Django By Example - Third Edition](https://www.packtpub.com/web-development/django-3-by-example-third-edition) Applications Together:

* [Part 1 - Building a Blog](https://github.com/ahuimanu/CIDM6325/tree/master/blog)
* [Part 2 - Building a Social Website](https://github.com/ahuimanu/CIDM6325/tree/master/bookmarks)
* [Part 3 - Building an Online Shop (eCommerce)](https://github.com/ahuimanu/CIDM6325/tree/master/myshop)
* [Part 4 - Building an E-Learning App and Chat Server using an API](https://github.com/ahuimanu/CIDM6325/tree/master/educa/educa)

I encourage you to hand-code from the book and resist the temptation to just copy and paste from the source files.

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

## Guide to Book Topics for Final Project (Baseline, Good, Better, Best)

I have classified the learning objectives from Antonio's book according to the following scheme.  Each category is relative to the following requirements for your final project:

* You must implement *all* **Baseline** components - Gets you to 70% of the value
* You must implement the required/demonstrated SEO tools - Gets you to 75% of the value (***FORTHCOMING***)
* You will implement *at least* six **Good** components - Gets you to 80% of the vaue
* You will implement *at least* three **Better** components - Gets you to 85% of the value
* You will implement *at least* one **Best** components - Gets you to 90% of the value

Where is the remaining 10%? It comes from the synthesis and service to your idea (implementation).

* **Baseline**: Essential Django knowledge that must be demonstrated in your final project
* **Good**: Fundamental knowledge that sets up a more useful app
* **Better**: Approaching a higher degree of robustness
* **Best**: Approaching professional-grade features and tools

Topic                                   | Baseline  | Good  | Better  | Best
---                                     | ---       | ---   | ---     | ---
***Chapter 1***                         |           |       |         |
Installation                            | x         |       |         |
Creating projects and apps              | x         |       |         |
Models, Views, Templates                | x         |       |         |
Routing                                 | x         |       |         |
Pagination in Views                     | x         |       |         |
Queries and QuerySets                   | x         |       |         |
***Chapter 2***                         |           |       |         |
Forms and ModelForm                     | x         |       |         |
Third-party integration                 | x         |       |         |
Sending emails                          |           | x     |         |
***Chapter 3***                         |           |       |         | 
Template Filters                        |           |       |         |
Sitemaps                                | x         |       |         |
Syndication                             |           | x     |         |
Postgres                                | x         |       |         |
Postgres Full-text search               | x         |       |         |
***Chapter 4***                         |           |       |         |
Django auth                             | x         |       |         |
Custom user model                       |           | x     |         |
Social auth integration                 |           | x     |         |
***Chapter 5***                         |           |       |         |
Advanced model relationships            | x         |       |         |
Frontend with JS and jQuery             |           | x     |         |
Custom decorators                       |           | x     |         |
Use JS/jQuery for AJAX                  |           |       | x       |
***Chapter 6***                         |           |       |         |
Many to Many relationships              | x         |       |         |
Django signals                          |           |       | x       |
Signals to track activity               |           |       | x       | 
key-value store with REDIS              |           |       |         | x
***Chapter 7***                         |           |       |         |
CRUD on objects                         | x         |       |         |
eCommerce catalog/cart/checkout/orders  |           | x     |         |
Django sessions/cookies                 |           | x     |         |
Custom context processing               |           | x     |         |
Celery/RabbitMQ/Flower for task queueing|           |       |         | x
***Chapter 8***                         |           |       |         |
Custom Admin Views                      |           | x     |         |
CSV handling                            |           | x     |         |
Payment gateways                        |           |       | x       |
PDF handling                            |           | x     |         |
***Chapter 9***                         |           |       |         |
i18n and l10n                           |           | x     |         |
Translation                             |           |       | x       |
Recommendation engine in REDIS          |           |       |         | x
***Chapter10***                         |           |       |         |
Fixtures for data loading               |           | x     |         |
Model inheritance                       | x         |       |         |
Custom model fields                     | x         |       |         |
Class-Based-Viewsd and Mixins           | x         |       |         |
Formsets                                |           | x     |         |
User groups and permissions             |           | x     |         |
***Chapter 11***                        |           |       |         |
User self registration                  | x         |       |         |
User-provided content                   | x         |       |         |
User uploads                            |           | x     |         |
Django caching                          |           | x     |         |
Memcached for caching                   |           |       | x       |
***Chapter 12***                        |           |       |         | 
Django REST Framework                   |           |       |         | x
API authentication                      |           |       |         | (x)
Serliaziation                           |           |       |         | (x)
API Permissions/Authorization           |           |       |         | (x)
Viewsets and Routing                    |           |       |         | (x)
Requests to consume APIs                |           | x     |         |               
***Chapter13***                         |           |       |         |
Django Channels                         |           |       |         | x
WebSockets (frontend)                   |           |       |         | x
REDIS for Channels implementation       |           |       |         | x
***Chapter14***                         |           |       |         |
VPS for deployment                      | x         |       |         |
Postgres (duplicate)                    | x         |       |         |
nginx, uWSGI, gunicorn                  | x         |       |         |
Static assets with nginx and whitenoise | x         |       |         |
Securing with SSL                       | x         |       |         |
Daphne for Channels                     |           |       |         | x
Custom middlewre                        |           |       | x       |
Task scheduling with cron               |           | x     |         |
***Extra***                             |           |       |         |
Deployment to a PaaS (Heroku)           |           |       | x       | 

## EXTRAS

There are also a few extra modules and/or applications in this repository that are shared in support of the course.

* [ETL Fixtures](https://github.com/ahuimanu/CIDM6325/tree/master/etl_fixtures): A python module to Extract, Transform, and Load T-100 Market data from a CSV file to a Django Fixture JSON file.
* [T-100 Data](https://github.com/ahuimanu/CIDM6325/tree/master/t100data): A Django Project that demonstrates loading and querying the T-100 Market data.

## Python Tips and Guidance

I will keep some general Python notes here:
* For [Visual Studio Code](https://code.visualstudio.com/), please use the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
* The Python Extension should help you to adhere to the [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) with its [linting](https://en.wikipedia.org/wiki/Lint_(software)) capabilities.

## Build a Blog Notes

Here are observations and notes from the chapters

## Chapter 1 - Build a Blog

---

* Make sure you install the latest version of any software the author refers to
    * For Python, you can go to [Python.org](https://www.python.org/)
    * For any packages, such as [Django](https://www.djangoproject.com/), you can consult the [Python Package Index](https://pypi.org/)
    * There are altneratives for **Virtual Environment** implementation, but making one is necessary regardless:
        * The book mentions `venv` which is a part of the standard Python 3.x install.  Note that the command is run like this: `python -m venv`
        * You can also install [miniconda](https://docs.conda.io/en/latest/miniconda.html) which is popular among the data science community.  I have started to use `miniconda` more lately.
    * **Virtual Environments** make a localized copy of Python and any libraries you use for your application so that they are separated from other applications.
        * virtual environments must be enabled and disabled
        * These are all command-line activities and I will be demonstrating this
    * **CLI options**:
        * _Windows_: I recommend that you install [Git For Windows](https://gitforwindows.org/) and use the **GitBash** command-line tool that comes with it
        * _Mac_: The built-in `terminal` App will work
        * **VS Code**: In all cases, try to do your terminal work from within VSCode's built-in terminal.

### Models

With `Django` you are persisting business data using [Object/Relational Mapping](https://en.wikipedia.org/wiki/Object-relational_mapping), which is a fairly standard approach to web application development.

This is there to structure your database.  Django Models are classes.  Review the basic structures and provisions of the [Python language](https://www.w3schools.com/python/default.asp).

### Admin

A great feature of Django is the built-in admin interface - you can perform CRUD operations here.

### Queries

There is a built-in query expression structure that saves time and avoids the need to write SQL directly in most cases.

### Views

We will try to use Class-Based-Views as much as possible.  However, Function-Based-Views are also possible.

### Secret Key

Django uses a SECRET_KEY for many security purposes in your project.  Since I will be encouraging the use of Github, publishing your secret key is a problem to avoid.  In fact, if you look at this repository, the initial commit contains a secret key (since changed).

Relevant part of the documentation: [The secret key must be a large random value and it must be kept secret.](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/#secret-key)

Also, since we'll use Git and Github, placing an effective GITIGNORE file into our repository is important: [Gitignore for a Django project](https://djangowaves.com/tips-tricks/gitignore-for-a-django-project/)

### Templates

Templates are HTML files with escapes to contain minimal display and presentation logic.  The _beauty_ of your pages will completely rely on one of a few options:
* Your skill with CSS
* Use of a robust component library
* Some template you find/purchase

## Chapter 2 - Enhancing Your Blog with Advanced Features

---

Antonio really adds in some useful features here and provides a fairly advanced use of Django within two chapters of the book:
* Email
* Comments
* Tags and metadata
* Recommendations

### Forms and Email

Django provides a few classes for working with Forms:
* [Form](https://docs.djangoproject.com/en/3.0/ref/forms/api/)
* [ModelForm](https://docs.djangoproject.com/en/3.0/ref/forms/models/)

There are a number of [FormFields](https://docs.djangoproject.com/en/3.0/ref/forms/fields/) that you include in your Form models to create a user interface.

**Passwords**
Immediately, Antonio starts to talk about using an email account.  Putting authentication information into your source files is a non-starter...

Let's use [DOTENV](https://pypi.org/project/python-dotenv/).  You can see how I handle this in the code.

**django shell**

Notice how Antonio opens the [django shell](https://docs.djangoproject.com/en/3.0/ref/django-admin/#shell) to quickly test email sending. The shell is very handy for this purpose and others.

`python manage.py shell`

**gmail and smtp**

If you use the gmail example from the book, it will likely fail due to the security you have with your account (2-factor and whatnot).  The solution is to use [App Passwords](https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637344913016438884-914897482&rd=1).

Or, try one of the approaches Antonio mentions.  

We will also explore using the free tier of services like [SendGrid](https://sendgrid.com/) or [MailChimp](https://mailchimp.com/)

### Comments and Tags

We see another application of foreign key, which reminds us that the Django ORM is there to help shape the tables in an RDBMS.

Don't forget to run `python manage.py makemigrations`

Also, if we want to use the Django Admin, we always need to register our new models with the admin:

``` python
from .models import Post, Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

```

**Models and Forms**

We can build forms straight from models, which is handy.

**Taggit**

By using the [Django Taggit](https://github.com/jazzband/django-taggit) app/library, you are getting your first taste of extending Django by using 3rd-party code, we will do more of this as time goes on.

Although Antonio specifies a version, if you install `django-taggit` without a version specified, it will install the latest: 

`pip install django-taggit`

***GOTCHA***: Make sure your virtual environment is active when you run the above.

You will notice that a significant amout of power comes from the [taggit app](https://django-taggit.readthedocs.io/en/latest/getting_started.html)

## Chapter 3 - Extending the Blog Application

---

Although very powerful as-is, in Chapter 3, Antonio rounds out the Blog app with the following features:
* Custom template tags and filters
* Sitemap and syndication (both useful for SEO)
* Full-text search in Postgres (will be difficult to do on desktop)

**Template Tags and Filters**

The templating system provides for dynamic content presentation on both the backend (with views and models) as well as in the front end with template tags and filters.

The Django Template Language has a number of [Built-in template tags and filters](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/)

However, a remarkable feature is the ability to extend these built-in tags and filters with your own custom versions.  In order to do so, we must create our own custom app to hold our customizations.

***GOTCHA***: Because our tag customizations are created in a django app, make sure restart the server after code changes to the tag customizations:
* `CTRL + C` to quit
* `python manage.py runserver` to restart

Custom template filters allow for further text processing as a Django Template is rendered.

* Recall that filters operate in the following manner: `variable|filter_name`
* You can also pass arguments to filters: `variable|filter_name:"arg"`

Django has a number of [built-in filters](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#built-in-filter-reference).


**Markdown Filter**

Earlier, I mentioned that this README utilizes [Markdown](https://daringfireball.net/projects/markdown/basics).

As a blog application, text input would be greatly enhanced by the use of markdown.  So, we turn to PIP to acquire [Markdown Capabilities](https://python-markdown.github.io/) for our Django Project.

To install: `pip install Markdown`

We can then create custom filters in our `blog_tags` app.

**Sitemaps**

SEO is significantly enhanced when you help Google's crawlers and spiders with a well-crafted sitemap.

Django facilitates this with `django.contrib.sites` and `django.contrib.sitemaps`

To generate sitemaps programmatically - which is common - allows for a responsive tailoring of how you reveal your site to Google et al.

Read more about [the sitemap framework](https://docs.djangoproject.com/en/3.0/ref/contrib/sitemaps/).

**Feeds**

Although social mediea (Facebook, Instragram, Twitter, etc.) have somewhat *regrettably* relegated syndication strategies like RSS and Atom, these are still useful features.

There are [built-in syndication features](https://docs.djangoproject.com/en/3.0/ref/contrib/syndication/) in Django: `django.contrib.syndication`

**Full-Text Search and PostGres**

[PostgreSQL](https://www.postgresql.org/) is a [Relational Database Management System](https://en.wikipedia.org/wiki/Relational_database#RDBMS) that is very full-featured, free, and open source.  It is also the preferred RDBMS in the Django community.

There are installers for Windows, Mac, and Linux.  Postgres will happily run on your local machine and, eventually, on your VPS.

To complete chapter 3, Antonio has us using Postgres for its full-text search capabilities.

***Windows Note***
The commands that Antonio shows at the end of chapter 3 will work on your VPS, but won't necessarily work as shown on windows. For windows, we will use pgAdmin, which is a browser-based management tool for PostgreSQL.  I will demo this in the video that goes along with this code and these notes.

**Settings**

The settings file needs to be adjusted to use Postgres.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'blog',
        'PASSWORD': '*****',
    }
}
```

DO NOT HARD-CODE THIS INFORMATION, use the dotenv approach.

**Fulltext Search**

The postgres contrib package makes this very easy.

---

# Bookmarks Social Site

Antonio moves on to cover several very useful aspects of Django and web development with this "social" site:

* Authentication
* Extending the user model
* Users and profiles
* Social authentication with [OAuth2](https://oauth.net/2/)
* REST services and [jquery's AJAX](https://api.jquery.com/Jquery.ajax/)
* Creating a following system
* using signals for event detection
* Using a caching mechanism with [Redis](https://redis.io/)

## Chapter 4 - Bookmarks

---

* Don't forget that Antonio provides all source code on the [Packtpub Github](https://github.com/PacktPublishing/Django-3-by-Example).
* You will need to draw on what you learned in the blog app.  For instance, in working with static files.
* To show the nuts-and-bolts, Antonio seems to use Function-Based-Views commonly, we'll want to refactor down the road to [Class-Based-Views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/).
* There are a number of pre-built CBVs for authentication that we should use for [user authentication in Django](https://docs.djangoproject.com/en/3.1/topics/auth/).

***NOTE:*** Over time, the packages you've installed in python will go stale.  Here are some notes about `conda` and `pip`:

* You can update conda itself with `conda update conda`
* You install an initial ***miniconda*** virtual environment this way: `conda create -n your_env python=x.x.x`
* you activate your virtual environments this way: `conda activate your_env`
* once active, use `pip install` as normal
* upgrade a pip package this way: `pip install package_name --upgrade`
* Also, as the author's book is frozen in time, like any book, you'll likely want to upgrade the packages he refers to using these commands.

**Extending the User Model**

There are a few things Antonio does that are common in the Django world but also, arguably, supplanted by more up-to-date techniques:
* Use of FBV over CBV (most advocate for CBV)
* Use of the default User object and [extension through a related Profile](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model)
* Extension of the [User model via in inheritance](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#substituting-a-custom-user-model).
* Both of these approaches are demonstrated in the book

**Custom Authentication Backend**

Often, and to avoid YAA/YAP (Yes Another Account/Yet Another Password), it might be good to avoid a localized account approach that the default authentication makes possible.

The `AUTHENTICATION_BACKENDS` setting allows for [multiple approaches](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#other-authentication-sources).  This allows for multiple inquiries for authentication in your app.

**Social Authentication**

A good example of multiple auth backends is in the book using `social-auth-app-django`.  However, `django-allauth` is also common and popular.  For instance, [Cookiecutter Django](https://cookiecutter-django.readthedocs.io/en/latest/) uses allauth.

Bear in mind that the `social-auth-app-django` is very likely updated.  Also, social-auth is very capable and the services provided by it [are now fairly commodity](https://python-social-auth.readthedocs.io/en/latest/backends/index.html#supported-backends).

For a fresh install, perhaps not specifying a version is best: `pip install social-auth-app-django`

***NOTE*** please note the `hosts` entry mentioned in Chapter 4.  The presages why it will be important to operate with a domain name soon and deploy.  How to create a hosts entry is discussed for the common platforms: Windows, Mac, and Linux.

Now that we are using named hosts, it is necessary to indicate to Django what IPs or hosts it is permitted to operate on:

`ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']`

When we are in DEBUG mode, all traffic is allowed, but when we deploy, it will be a different matter.

***HTTPS Required***

Over the last few years, it has become absolutely necessary to ensure that your site is served using HTTP (via TLS/SSL).  In fact, your site will be negatively scored by Google and Bing if you aren't serving traffic via HTTPS.  Once we setup deployment and proxy services through NGINX, this will be handled for us.  However, the chapter mentions setting up [RunServerPlus]() for an extended development experience.

**Social Backends**

Authentication examples using Facebook, Twitter, and Google are demonstrated.

## Chapter 5 - Images

---

Lots of great new features in this chapter.  Quick notes:

* don't forget that a **slug** is a quick phrase associated with an item. 
* We use the `slugify` utility to derive a slug from an image name.
* I've included a 'home' app so that when you start the server, there is some page that loads.

The command to run your app with RunServerPlus is: `python manage.py runserver_plus --cert-file cert.crt`

### Many to Many Relationships

The Django ORM handles [many-to-many relationships](https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/) particuarly well.

### Form Validation
Django allows you to define form methods to clean specific fields using the clean_<fieldname>() convention. [More on form and field validation](https://docs.djangoproject.com/en/3.1/ref/forms/validation/).

### The necessity of client-side code

Although some would argue that [jQuery](https://jquery.com/) is passé, it still performs valuable client-side services and utilities that are often easier to implement as opposed to [Vanilla JavaScript](http://vanilla-js.com/).  Again, I acknowledge that this is debatable.

The creation of the "Bookmarklet" requires that we use client-side code.  Honestly, this part will be fairly tricky and ramps up the breadth and depth of tools we employ.

Although this code is complex, it is also clever and does really work.

### thumbnails

Thumbnails are an important aspect that should be automated if at all possible.  Fortunately, [PIPY](https://pypi.org/) has a choice of solutions.

Antonio has used [easy thumbnails](https://pypi.org/project/easy-thumbnails/) in the bookmarks project.  [Easy thumbnails](https://easy-thumbnails.readthedocs.io/en/latest/) is a great example of the immediate power you have available by including code from the Python community. This is among the reasons that [Python](https://www.python.org/) has become a [favorite language in the data science and data analytics realm and beyond](https://www.howtopython.org/why-python-programming-language-popular-2020/).

### AJAX 

Part of why we use client-side [JavaScript](https://developer.mozilla.org/en-US/docs/Glossary/JavaScript) libraries like [jQuery](https://jquery.com/) is to make asynchronous/out-of-process calls back to the server from the client. Formalized as [Asynchrous JavaScript and XML](https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX), AJAX represents the process of making such calls and was the driving factor behind the [Web 2.0 phenomenon](https://en.wikipedia.org/wiki/Web_2.0).  This makes AJAX essential learning and constitutes a necessary tool in our toolset.

As a client-side technology, it is necessary to identify the dependency in our `base.html` template:

***NOTE:*** try to use the latest version of jQuery.  As Antonio is using [Google hosted libraries](https://developers.google.com/speed/libraries/) in the code below, you can go there to get the latest and greatest.  Such a resource is known as a [Content Delivery Network](https://en.wikipedia.org/wiki/Content_delivery_network) and holds the advantage of being available on a fast server and also likely cached within the browsers of end users.

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
  $(document).ready(function(){
    {% block domready %}
    {% endblock %}
  });
</script>
```

**The Document Object Model**

Primarily, we use JavaScript/jQuery both for [Document Object Model](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) (DOM) manipulation and for AJAX.  As such, the above code ensures that the DOM has fully loaded prior to attempting operations on it.

### Cross-Site Request Forgery

As is usually the case with most technologies, they present a double-edged sword where the source of power and benefit can also be the [source of risk and harm](https://developer.mozilla.org/en-US/docs/Web/Security).  Django provides good protection against [Cross-Side Request Forgery](https://developer.mozilla.org/en-US/docs/Glossary/CSRF) for forms and also provides the means to develop [custom CSRF techniques for AJAX](https://docs.djangoproject.com/en/3.1/ref/csrf/#ajax).

### Custom View Decorators

Although django provides an ability to detect whether a POST (or any HTTP request) was made with [XMLHttpRequest](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest) using the [`is_ajax`](https://docs.djangoproject.com/en/3.1/ref/csrf/) method, we will simplify this with a [Python Decorator](https://www.python.org/dev/peps/pep-0318/).

### Adding AJAX Pagination

Another adjantage of client-side AJAX is the ability to create an [infinite scroll](https://www.seoclarity.net/blog/pagination-vs-infinite-scroll), which is a common and popular UI choice. Antonio extends his code to handle either standard or AJAX pagination.

## Chapter 6 - Follow and Tracking

---

The feature list in this chapter goes even deeper.  

### Building the Follow System

Although the Django ORM handles [many-to-many relationships](https://en.wikipedia.org/wiki/Many-to-many_%28data_model%29) with the [ManyToManyField](https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/), there are times when it becomes necessary to also associate data with the link between the two models.

In the chapter, Antonio establishes a `Contact`entity to describe the relationships between users.

**Custom User Model**
Antonio again reminds us that a well-planned [custom user model](https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model), established up-front and early in the project, is the best approach as opposed to the [monkey patching](https://en.wikipedia.org/wiki/Monkey_patch) (an actual term in the Python community) he demonstrates with the `Profile` class.


**ABSOLUTE_URL_OVERRIDES**
The app creates a detail page for each user using the `ABSOLUTE_URL_OVERRIDES` setting in Django.  This is useful as we use the `get_absolute_url()` method to get a URL per object from the Django ORM.

### Building the Activity Stream

Tracking user actions and making them available as an activity stream is a common feature of social websites.

**Content Types Framework**

Django provides the contenttypes framework to work with the modles in your project/app.  This is a form of [introspection](https://book.pythontips.com/en/latest/object_introspection.html) or reflection that allows meta-awareness within your application.

Content Type is also useful to manage more complex relationshps between models in your application.

### Denormalization

The most common reason to denormalize data is for performance.  The price is the potential for a loss of management and stability that the Django ORM and an RDBMS provide.

[Django Signals](https://docs.djangoproject.com/en/3.1/ref/signals/) allow for notification when an internal action will take place such that you may take action, often before and after, to accomplish some task.

This is done in the example to develop a running tally of total likes.

### App configuration

We often add the AppConfig class when using URLs, but haven't discussed it much yet.  AppConfig is a part of the [Django Application Configuration](https://docs.djangoproject.com/en/3.0/ref/applications/) tools available.

These tools are useful to specify signal receiver functions.

### REDIS for in-memory database function

Directly from Antonio:

> Redis is an advanced key/value database that allows you to save different types of data. It also has extremely fast I/O operations. Redis stores everything in memory, but the data can be persisted by dumping the dataset to disk every once in a while, or by adding each command to a log. Redis is very versatile compared to other key/value stores: it provides a set of powerful commands and supports diverse data structures, such as strings, hashes, lists, sets, ordered sets, and even bitmaps or HyperLogLogs.

**Redis installation**

REDIS does not come with a convenient installer in the case of Windows and even Mac, to a degree.

Cases:
* If on Windows, [this reference] is good but assumes installation of the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10#install-the-windows-subsystem-for-linux).

Although I will demonstrate this, using REDIS is entirely optional.

---

# Windows Subsystem for Linux

The desire for Unix on Windows is as old as windows.  With Windows 10, a very viable approach, thanks to virtualization and contemporary hardware, is possible using the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/).  Of particular advantage is to be able to run an environment that is identical to a remote envoronment. There are sections of [Antonio Mele's book](https://github.com/PacktPublishing/Django-3-by-Example) where the ability to do this would be beneficial:

* Postgres
* Redis

Better still, we can adopt a hybrid approach to using Visual Studio Code such that we can connect to our WSL linux install locally and use all the tooling and commands you'd use in the Ubuntu Linux environment.  This allows us to run all of the same commands that [Antonio Mele](https://github.com/PacktPublishing/Django-3-by-Example) does in the [book](https://www.packtpub.com/product/django-3-by-example-third-edition/9781838981952).

## Working with VS Code

This is the integration I really wanted to show you: [Get started using Visual Studio Code with Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode)

## Mac or Linux

With a Mac, you'd want to look into [homebrew](https://brew.sh/), which will get packages for you the way the [Advanced Package Tool (apt)](https://geek-university.com/linux/advanced-packaging-tool-apt/) would in [Ubuntu](https://ubuntu.com/).

---

# Online Shop

The online shop has a number of very practical use-cases for Django and Python:

* Product catalog management
* [Django Sessions](https://docs.djangoproject.com/en/3.1/topics/http/sessions/) to track shopping cart state.
* [Django Celery](https://docs.celeryproject.org/en/stable/django/) for managing background and asynchronous tasks
* Payment Gateway integration using [Braintree](https://www.braintreepayments.com/)
* Exporting/Serializing data
* Generating PDFs
* Internationalization

## Chapter 7 - Creating an Online Shop Project

We cover some basics, some of which we've covered before, and some that are new:

* Creating the product catalog models, adding them to the administration site, and building the basic views to display the catalog
* Building a shopping cart system using Django sessions to allow users to keep selected products while they browse the site
* Creating the form and functionality to place orders on the site
* Sending an asynchronous email confirmation to users when they place an order

Ensure that you create your virtual environment:

```
mkdir env
python -m venv env/myshop
source env/myshop/bin/activate
```

Try to keep your virtual environments together.

### Product Catalog

This section is a straight-forward review of most of what was covered in *blog* and *bookmarks*.  Still, it is very handy to have an example of showing a catalog of items for viewers to peruse.

### Shopping Cart and Django Sessions

The issue with the World Wide Web is that the HTTP/HTTPS protocols are "stateless."

![HTTP Stateless](https://i.imgur.com/3BdgRVN.jpg)

Practically, this means every question is "forgotten" by the server and client unless steps are taken to ensure some record of the conversation.

There are two main ways to get around this:

* Cookies / LocalStorage ("memory" lies on the client side - aka browser)
* Sessions ("memory" lies on the server side perhaps with some client-side help)

![Cookies as a Solution](https://i.imgur.com/3FZRIC2.jpg)

Sessions are Key-Value pairs, stored against an ID.  Often, the ID will be kept in a cookie, but that is not always necessary as cookies may be entirely disabled on the client side.

![Session Variables as a Solution](https://i.imgur.com/T7rHEaF.png)

#### Django Sessions as Middleware

[Django's Middleware Framework](https://docs.djangoproject.com/en/3.1/topics/http/middleware/) provides a means of "intercepting" any [Request / Response](https://docs.djangoproject.com/en/3.1/ref/request-response/) cycle to further check and apply rules for the overall operation of your application. Django Sessions are implemented using Middleware.

In your application, session variables and values are stored as [Python Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries).

So, we can read/write from the session collection simply:

``` python
# write
request.session['foo'] = 'bar'

# read
request.session.get('foo')

# delete
del request.session['foo']
```

#### Django Sessions Settings

The MIDDLEWARE list in `settings.py` should already contain `'django.contrib.sessions.middleware.SessionMiddleware'` using the default *startproject* command with *django-admin*.

As there a number of strategies to manage the session variables on the server side, we also have a `settings.py` option to establish the `SESSION_ENGINE`.

By default, Django uses the database and a built-in *Session* model which is defined in the *django.contrib.sessions* application found in a default install of Django.

However, the other strategies are:

* **Database sessions**: Session data is stored in the database. This is the default session engine.
* **File-based sessions**: Session data is stored in the filesystem.
* **Cached sessions**: Session data is stored in a cache backend. You can specify cache backends using the CACHES setting. Storing session data in a cache system provides the best performance.
* **Cached database sessions**: Session data is stored in a write-through cache and database. Reads only use the database if the data is not already in the cache.
* **Cookie-based sessions**: Session data is stored in the cookies that are sent to the browser.

#### Related Settings

We can further control the behavior of Sessions on the server with the following entries in the `settings.py` file:

* **SESSION_COOKIE_AGE**: The duration of session cookies in seconds. The default value is 1209600 (two weeks).
* **SESSION_COOKIE_DOMAIN**: The domain used for session cookies. Set this to mydomain.com to enable cross-domain cookies or use None for a standard domain cookie.
* **SESSION_COOKIE_SECURE**: A Boolean indicating that the cookie should only be sent if the connection is an HTTPS connection.
* **SESSION_EXPIRE_AT_BROWSER_CLOSE**: A Boolean indicating that the session has to expire when the browser is closed.
* **SESSION_SAVE_EVERY_REQUEST**: A Boolean that, if True, will save the session to the database on every request. The session expiration is also updated each time it's saved.

#### Serialization

As was the case in the T-100 project for Assignment 4.5, it is commonly the case that some form of [serialization](https://docs.djangoproject.com/en/3.1/topics/serialization/) is needed to extract and load data into the O/RM.  This same strategy is in use when working with sessions as [Django will serialize values and objects as JSON](https://docs.djangoproject.com/en/3.1/topics/serialization/).  Therefore, every session variable value you store will be serialized as [JSON](https://docs.python.org/3/library/json.html).

#### Context Processors

When we pass a request into our views, we may also establish a [context so that we can pass along additional information to our templates for rendering](https://docs.djangoproject.com/en/3.1/ref/templates/api/#playing-with-context-objects).  There are various [built-in context processors](https://docs.djangoproject.com/en/3.1/ref/templates/api/#built-in-template-context-processors) and we also have the ability to adjust context processing.

### Registering customer orders

When a cart is ready to be finalized, it needs to transition to an invoice/order such that payment and shipping (if applicable) processes may proceed.  Further, this order needs to be recorded as it is possible that the products purchased may one day no longer reside in the catalog.

In this section, Antonio shows us how to use [inline admin models/views](https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#inlinemodeladmin-objects) which makes master/detail management easier.  

![InLine Admin Models](https://i.imgur.com/dN37nbY.png)

#### Creating a Customer Order

The general steps for placing an order include:

* Present a user with an order form to fill in their data
* Create a new `Order` instance with the data entered, and create an associated `OrderItem` instance for each item in the cart
* Clear all the cart's contents and redirect the user to a success page

### Launching asynchronous tasks with Celery

When we discussed how the web is stateless, another limitation to overcome is the inherent latency of using networking protocols.  The [Open Systems Interconnection (OSI )Model](https://en.wikipedia.org/wiki/OSI_model) describes how network protocols interoperated at various "layers" required to initiate and receive networked data communications.

This creates a "stack" of communication coordination and, despite the fast speed of electrons across transmission media, it is not instantaneous.  Further, the speed of communications on your local device/computer will always be faster than the speed of data communications across any network media as the distance to cover is neglible within the device.

![HTTP Network Communications Stack](https://i.imgur.com/Hp3Qsme.jpg)

In our app, we'd like to send responses to the user as quickly as possible and let the server execute some process asynchronously. The server will do this asynchronously often when some data Input/Output needs to occur, particularly so when network communications are required.

However, this is also relevant for time-consuming processes or processes subject to failure at runtime.  In the eCommerce/"myshop" application, it will make sense to send a receipt for the order using email. As we will use Simple Mail Transfer Protocol (SMTP) to send the email, there are various causes of latency and failure that make it prudent to decouple the process for sending an email from the rest of the Django architecture and processing. We want to launch an asynchronous tasks to prevent blocking further code execution.

In this chapter, Antonio shows us how to use [Celery](http://docs.celeryproject.org/en/latest/index.html) as a distributed task queue for message processing. Celery provides an ability to launch asynchronous tasks on demand or scheduled to be run at a specific time.

### Celery Installation

As is the case with almost everything else in Python/Django, we use `pip` to [obtain celery from PyPi](https://pypi.org/project/celery/).

#### RabbitMQ

We need additional software to work with Celery for message queueing.

Antonio explains:

> Celery requires a message broker in order to handle requests from an external source. A message broker is used to translate messages to a formal messaging protocol and manage message queues for multiple receivers, providing reliable storage and guaranteed message delivery. You use a message broker to send messages to Celery workers, which process tasks as they receive them.

Much like [Postgres](https://www.postgresql.org/) or [Redis](https://redis.io/), [RabbitMQ](https://www.rabbitmq.com/) needs to be [installed separately](https://www.rabbitmq.com/download.html) and this process differs depending on what Operating System you work with.

***CAUTION***: As was the case with Postgres and Redis, this also means that the instructions that Antonio shows in the book assume a Linux environment (or perhaps a Mac environment).  The Windows installation process will differ.

Of the two installation methods listed for windows:

* [Chocolatey](https://chocolatey.org/) - [Installation with Chocolatey](https://chocolatey.org/packages/rabbitmq)
* [Windows Installer](https://www.rabbitmq.com/install-windows.html)

I've chosen *chocolatey*. The [Windows Installation Guide](https://www.rabbitmq.com/install-windows.html) also highlights a common side-effect of using various tools to assemble a modern web application in that there are many dependencies, which makes for many sources of trouble and occassions for trouble-shooting.

A prime example is RabbitMQ's reliance on [Erlang](https://www.erlang.org/).

I suspect that a similar approach on Mac, using [homebrew](https://brew.sh/), is best there.

Antonio presents that the following command will run RabbitMQ, and for Mac/Unix/Linux, he is correct:

`rabbitmq-server`

However, as is usually the case, on Windows it is different.

As I mentioned, I used the Chocolatey install method [mentioned at the RabbitMQ website](https://www.rabbitmq.com/install-windows.html#chocolatey).

Further, I would take care as most of how you run on windows is through batch files, just as is the case with `venv` and its `Scripts` directory.

I have found that just running RabbitMQ from its install directory with an elevated CMD or PowerShell shell is sufficient.

For me, the install path is `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.8.5\sbin` which should also be the case on your machine.

From what I can gather, once installed, RabbitMQ seems to just run as a Windows Service at startup.

For this reason, much as is the case with PgAdmin4, you can simply point a browser to the admin interface for RabbitMQ and you can monitor its function and perform administrative tasks.

The admin interface is running here for me: `http://localhost:15672/#/`

***Massive VS Code Annoyance***

It would seem that pylint can't see some of our own project's elements and underlines the code with a "red squigelly" saying that `Order has no members` or some such message.

This helped:

In case of a Pylint error, install the following
```
pipinstall pylint-django
```

Then create a file, .pylintrc, in the root folder of your project and write the following

```
load-plugins=pylint-django
```

#### Celery and Django

Although Django has built-in support for Celery, as it is a common task queue tool used in the Django world, there are specific configuration aspects unique to Django.  

Antonio's code follows these steps, however, if you wish to use the latest version of Celery (5.0.0 in October 2020), then I would still review the Celery documentation:

[First Steps with Django](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)

***Celery Update***

The most current version of Celery is 5.0.0.  The [5.0.0 documentation seems to recommend](https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-the-shared-task-decorator) the use of the `shared_task` decorator rather than the `task` decorator. You can simply use the older version of celery that Antonio specifies if you wish to avoid these changes. This is EXACTLY why Antonio is specific with versions throughout his code.  When I use `shared_task` with Celery 5.0.0, the code runs fine.

#### EMAIL BACKEND

Don't forget (covered in Antonio's Chapter 2) that if you do not plan to wire up to an SMTP mail server during development, then Django provides a console email backend for testing. Without setting this, the built-in email provisions in Django will try to use your local machine to send an email, which will not succeed unless you have explicitly set this up (which is very unlikely).

Here is what you want to ensure is added to your `settings.py` file:

```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

***Case Sensitivity***
It might be the case that the following instruction from Antonio in Chapter 7:

`celery -A myshop worker -l info`

Might need to be changed to:

`celery -A myshop worker -l INFO`

As the -l instructs what log level to use and the lower-case version may not work.  This could be a windows thing.

Once Celery, RabbitMQ, and Django are working together, you can see evidence of the EMAIL_BACKEND working:

![Celery, RabbitMQ, and Django](https://i.imgur.com/Ad92HzZ.png)

### Monitoring Celery

Of course, having the command-line version of celery running is fine, but keeping a console up and running to monitor Celery and RabbitMQ might not be ideal.  For this, Antonio suggests that we install [Flower](https://pypi.org/project/flower/) to monitor [Celery](https://pypi.org/project/celery/).

`pip install flower`

This would arguably be an optional step.

Further, Flower does not support Celery 5.0.0 as of October 2020. 

Again, this is a **perfect illustration** of why Antonio puts specific versions into his tutorials/chapters.

## Chapter 8 - Managing Payments and Orders

Antonio brings another set of very useful features that would potentially work well with your own project ideas:

* Integrate a payment gateway into your project
* Export orders to CSV files
* Create custom views for the administration site
* Generate PDF invoices dynamically

### Payment Gateways

If you want to make money on the web, you will eventually be faced with working with Payment Gateways. In some cases, you can work more directly with services like [PayPal](https://developer.paypal.com/home/) or [Stripe](https://stripe.com/docs/api), but there are other services that provide aggregation of multiple payment methods, and Antonio has us focus on and use [Braintree](https://www.braintreepayments.com/).

#### Braintree Sandbox Account

Common among payment gateways is to provide a sandbox within which a developer may test their payment implementation using fake transactions and card numbers.  It is usually a trivial matter to then simply switch on the "live" version.

When you fill out the signup form, I suppose you can use CIDM 6325 as the Company Name, or use anything you'd care to.

![Braintree Signup](https://i.imgur.com/Kclzl1H.png)

Once you do the "confirm your account" email dance, you will be provided with a dashboard and the important credentials that your app can use to communicate with the payment gateway.

![Braintree Credentials](https://i.imgur.com/aHMYmZg.png)

#### Braintree Python Integration

There is a Python module for braintree that we can install using pip:

`pip install braintree`

And several settings to load into `settings.py` for the project:

***WARNING*** DO NOT PUT ACTUAL VALUES INTO YOUR SETTINGS FILE, USE DOTENV!!!

``` Python
# Braintree settings
BRAINTREE_MERCHANT_ID = 'XXX'  # Merchant ID
BRAINTREE_PUBLIC_KEY = 'XXX'   # Public Key
BRAINTREE_PRIVATE_KEY = 'XXX'  # Private key
import braintree
BRAINTREE_CONF = braintree.Configuration(
    braintree.Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)
```

### Integrating the payment gateway

Antonio has us create a new app so that we can proceed through the general steps of working with payments:

* Add items to the shopping cart
* Check out the shopping cart
* Enter credit card details and pay

Antonio also introduces the concept of using a redirect to communicate with the payment gateway code.  We also use sessions to store the order id.  Lastly, all of this assumes that celery is running.  For these reasons, this material is cumulative.

#### Integrating Braintree using Hosted Fields

Pay careful attention to how Antonio describes working with hosted fields and braintree:

> The Hosted Fields integration allows you to create your own payment form using custom styles and layouts. An iframe is added dynamically to the page using the Braintree JavaScript software development kit (SDK). The iframe includes the Hosted Fields payment form. When the customer submits the form, Hosted Fields collects the card details securely and attempts to tokenize them. If tokenization succeeds, you can send the generated token nonce to your view to make a transaction using the Python braintree module. A token nonce is a secure, one-time-use reference to payment information. It allows you to send sensitive payment information to Braintree without touching the raw data.

Antonio proceeds to outline the specific steps:

* In the view, a client token is generated using the braintree Python module. This token is used in the next step to instantiate the Braintree JavaScript client; it's not the payment token nonce.
* The view renders the checkout template. The template loads the Braintree JavaScript SDK using the client token and generates the iframe with the hosted payment form fields.
* Users enter their credit card details and submit the form. A payment token nonce is generated with the Braintree JavaScript client. You send the token to your view with a POST request.
* The payment view receives the token nonce and you use it to generate a transaction using the braintree Python module.

Often, the payment gateway service will provide you [fake credit cards to use in their sandbox](https://developers.braintreepayments.com/guides/credit-cards/testing-go-live/python).

Those are the basic steps and it is all quite easy.

Some issues to bear in mind:

* Antonio's example doesn't show you how to handle payment delines, but he does [point to the documentation](https://developers.braintreepayments.com/reference/general/processor-responses/authorization-responses).
* Antonio waits until the end of the book (which is what I should have done) to show how to take all of his applications Live, including how to [take payments into live production](https://developers.braintreepayments.com/start/go-live/python) as well.

### Exporting orders to CSV files

As I demonstrated in the T-100 project, Comma-Separated Values files are useful for imports and exports of data.  As such exports are typically an administrative function, Antonio shows us how to use the admin dashboard to get a CSV export of our orders.

#### Custom Admin Action

We create a custom admin action for CSV export that accepts:

* The current ModelAdmin being displayed
* The current request object as an HttpRequest instance
* A QuerySet for the objects selected by the user

The ability to export data as CSV is quite handy and something I've always really liked about Python and Django's ["batteries included"](https://www.python.org/dev/peps/pep-0206/) approach.  This is perfect for business students taking a computing degree that is business oriented.

### Extending the administration site with custom views

While the CSV export is very handy, Antonio also shows us how to customize the admin view in order to extend the capabilities of the admin app.

While we create a new admin template and view with Antonio, he reminds use that we can override any of the built-in admin templates as well: [https://github.com/django/django/tree/3.0/django/contrib/admin/templates/admin](https://github.com/django/django/tree/3.0/django/contrib/admin/templates/admin)

### Generating PDF invoices dynamically

Right along with the ability to work with CSV files is the ease with which we can produce PDF files as well.

The [Django documentation covers this topic](https://docs.djangoproject.com/en/3.0/howto/outputting-pdf/) and demonstrates the use of *ReportLab* for the purpose of PDF generation.

However, with the above approach, any PDF styling would be our responsibility.  Antonio recommends we use [WeasyPrint](https://weasyprint.readthedocs.io/en/latest/install.html) as it is good at rendering a PDF from our Template Layouts.

`pip install WeasyPrint`

***Windows Notes***

You will certainly further your education in the intricacies of working on multiple platforms with all of what we are working with and leanring about.  Specifically, the installation of [WeasyPrint on Windows](https://weasyprint.readthedocs.io/en/stable/install.html#windows) requires some additional care.

Follow these intructions thoroughly.

## Chapter 9 - Coupons, Discounts, and Internationalization

The biggest components of this chapter are [I18N](https://en.wikipedia.org/wiki/Internationalization_and_localization) and the recommender system.

The coupon example is useful but mainly from the standpoint of how to introduce new features across several apps, models, views, templates, etc.

### Internationalization (i18n) and Localization (l10n)

While a significant proportion of the Intenet and World Wide Web's earliest days often assumed the use of English and Western character sets, the need to adjust content to facilitate users from a variety of native toungues and cultures is obvious as the Internet and World Wide Web is a global resource.  To wit, the number of [native Mandarin speakers](https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers) is quite large and the [number of Internet users in China is equally quite large](https://en.wikipedia.org/wiki/List_of_countries_by_number_of_Internet_users) - *hint*: both are, respectively, the largest groups in class.

#### Django Support for i18n and l10n

Django is built with significant facilities to [accommodate i18n, l18n](https://docs.djangoproject.com/en/3.1/topics/i18n/), and [timezone management](https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/), all of which are of concern when your site may reach a broad spectrum of visitors and users. 

We start with the creation of message files that make it clear which text should be translated/localized.

The message files have a `.po` extension and, once compiled and translated, take on the `.mo` extension.

Further, the `manage.py` utility recognizes the `makemessages` and `compilemessages` commands to work with i18n and l10n.

The built-in i18n and l10n capabilities do rely on the GNU open-source `gettext toolkit`.

* For Mac, it is recommended to use homebrew for these purposes.
* For Windows, [Django provides these instructions](https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#gettext-on-windows).

***Process***

Antonio outlines the process fairly well:

1. Mark strings for translation in code and templates
2. Run `python manage.py makemessages`
3. Obtain translations and then run `python manage.py compilemessages` to generate the `.mo` files

This provides Django an opportunity to provide i18n and l10n services.  Django will examine whether `LocalMiddleWare` is enabled in your `settings.py` file or examine a `LANGUAGE_CODE` setting if enabled.

### Enabling i18n

Antonio covers a case of the use of Spanish and English.  The book is fairly instructive throughout this section so I have few additional notes to add.

### Recommender System

This section is optional as it covers REDIS.  This is a worthwhile section, but I am not requiring it due to the technical overhead of running REDIS on your local machine.

# E-Learning Platform

We made it! This is the final project that Antonio shows and I believe Antonio has show signficant value in the number of highly practical demonstrations he has provided of a modern and Python-drive framework like Django.

Antonio really ends with a finale here as he covers sevaral advanced features of Django:

*Chapter 10*:

* Fixtures to load data (we previewed this in the T-100 project)
* CBVs and Mixins (I covered this early as well)
* Formsets
* User groups and permissions
* Content Management System (I will also mention [Wagtail](https://wagtail.io/))

*Chapter 11*:

* Caching with Memcached
* Django cache framework
* Monitor and modify Memcache behavior

*Chapter 12*:

* Using the Django Rest Framework
* Specifying serializers
* Using the Python Requests library

*Chapter 13*:

* Django Channels to consume your REST API
* Using WebSocket (A front-end technology)
* Redis (optional)
* Work with the asynchronous capabilities of Django 3.x

## Chapter 10 - Building an E-Learning Platform

Antonio starts off with a "good" approach as has been the case with all of his projects, where just the basic elements are reviewed.

In preparation, Antonio sets up the follow models and adds them to the Django Admin:

* Subject
* Course
* Module

This is done in a manner that is consistent with each of the previous projects.

### Fixtures

We saw fixtures in the T-100 project.  They are a way to load data into your Django models in the database.  As I covered in the T-100 project, Django will use any of the following serialization formats to accept a fixture:

* [JSON](https://en.wikipedia.org/wiki/JSON)
* [XML](https://en.wikipedia.org/wiki/XML)
* [YAML](https://en.wikipedia.org/wiki/YAML)

Whereas I took [CSV](https://docs.python.org/3/library/csv.html) files in the T-100 projects and used Python to transform them into the JSON fixture files, Antonio shows that we can export data we create with the Django admin as fixtures and then re-import them.  As such, this is a strategy to backing up the data in a Django website/application.

We accomplish export and import with the following options to the `manage.py` script:

* `dumpdata`
* `loaddata`

We can then create a `fixtures/` subdirectory where fixture files will be automatically found.

Applications of fixtures include testing, pre-loading data, and backup/restore.

### Model Inheritance

[Inheritance](https://en.wikipedia.org/wiki/Inheritance_(object-oriented_programming)) is an [Object-Oriented](https://en.wikipedia.org/wiki/Object-oriented_programming) concept but comes in handy both in the use of Django Templates but also in model specification.  This allows for diversifation and specificity as your project evolves.

The implementation of Model Inheritance varies according to options available to specify how the database will structure the inheritance relationships:

* ***Abstract models***: Useful when you want to put some common information into several models.
* ***Multi-table model inheritance***: Applicable when each model in the hierarchy is considered a complete model by itself.
* ***Proxy models***: Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options.

BTW, this is very similar to the same strategies in [Microsoft's Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/modeling/inheritance).

#### Abstract Models

From Antonio:

>An abstract model is a base class in which you define fields you want to include in all child models. Django doesn't create any database tables for abstract models. A database table is created for each child model, including the fields inherited from the abstract class and the ones defined in the child model.

The principle approach is to us the internal "Meta" class in a Django model to specify metadata according to this description from the [Django Docs](https://docs.djangoproject.com/en/3.1/topics/db/models/#meta-options):

>Model metadata is “anything that’s not a field”, such as ordering options (ordering), database table name (db_table), or human-readable singular and plural names (verbose_name and verbose_name_plural). None are required, and adding class Meta to a model is completely optional.

So, we indicate that a Model class is abstract with this entry into `class Meta:`

`abstract = True`

This is Antonio's example:

``` python
from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Text(BaseContent):
    body = models.TextField()

```

Antonio uses this approach in the chapter.

#### Multi-table model inheritance

If a table-per-model approach is desired, then this is the way to go.  Antonio explains:

>In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model. To use multi-table inheritance, you have to subclass an existing model. Django will create a database table for both the original model and the sub-model. 

This is somewhat default behavior as simple Python-level inheritance is used:

``` python
from django.db import models

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class Text(BaseContent):
    body = models.TextField()
```

#### Proxy models

Whereas an abstract model simply provides the fields that a child model should assume and write to its table, a proxy model creates a single table from which both the parent and child model may operate.

>A proxy model changes the behavior of a model. Both models operate on the database table of the original model. To create a proxy model, add proxy=True to the Meta class of the model. 

``` python
from django.db import models
from django.utils import timezone

class BaseContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class OrderedContent(BaseContent):
    class Meta:
        proxy = True
        ordering = ['created']
    def created_delta(self):
        return timezone.now() - self.created

```

### Creating custom model fields

In most cases, the [built-in Model field types](https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types) will be sufficient for most needs.  However, Antonio demostrates how to create custom model fields to provide more specific behaviors.

More information on [custom model fields](https://docs.djangoproject.com/en/3.1/howto/custom-model-fields/) is available in the [Django Documentation](https://docs.djangoproject.com/).

### Creating a CMS

This is a massive topic that Antonio greatly reduces for orientation.  There are a number of very mature CMS applications that you can add into your Django project.  My recommendation would be the [Wagtail CMS](https://wagtail.io/).

For simplifiation, Antonio introduces the following features for his "mini" CMS:

* Log in to the CMS
* List the courses created by the instructor
* Create, edit, and delete courses
* Add modules to a course and reorder them
* Add different types of content to each module and reorder them

### Managing course modules and their contents

Antonio moves on to specifying what should go into the contents of a course by working with modules.

The complexity of this task requires that we manage multiple form objects on the same page using groupings called [formsets](https://docs.djangoproject.com/en/3.1/topics/forms/formsets/).  Since Django also has the ability to shape a form based on a model using [ModelForm](https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/), there is also a provision for creating [Model formsets](https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#model-formsets).

I respect Antonio's decision to use both jQuery and jQueryUI in his examples as they are tried-and-true technologies.  That said, [modern JavaScript](https://developer.mozilla.org/en-US/docs/Glossary/JavaScript), [JavaScript frameworks](https://medium.com/javarevisited/10-of-the-most-popular-javascript-frameworks-libraries-for-web-development-in-2019-a2c8cea68094) and [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) have relegated this approach to some degree.  

## Chapter 11 - Rendering and Caching

Caching is an important performance component of any web application as we use the Python language, runtime, and library to build our pages using Django.  As such, if the same the same "rendered" question is asked repeatedly, then building that page programmatically becomes a redundant waste of resources.  Thus, a caching strategy, where the already-rendered HTML/CSS/JS combo (which is ALL we ever send to the client/browser) is stored for delivery, is essential for performance.

Notice also in this chapter that Antonio points how to use [annotate()](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#annotate) to approximate SQL's [GROUP BY](https://www.w3schools.com/sql/sql_groupby.asp) as well as aggregate operations like [Count()](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#count). You've seen both of thes in the T-100 project.

Also in this chapter, Antonio more fully embraces and utilizes Django's [Class-Based Views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/).

BTW, it is possible to use memcached on Windows by simply downloading it from what one the links in this [blog post](https://commaster.net/posts/installing-memcached-windows/). Once downloaded, simply run it without the extra parts that Antonio mentions (no need to type `memcached -l 127.0.0.1:11211`): so, in a separate CMD or PS window, type `memcached.exe` and that's it.

With that, you can run the rest of the code.

## Chapter 12 - Django REST Framework

Although this is bonus territory, I am very pleased that Antonio is covering DRF in this chapter and Channels in the next.  Both are 3rd party tools but enable very modern and up-to-date approaches.

As such, this is an outstanding tour of features:

* Install Django REST framework
* Create serializers for your models
* Build a RESTful API
* Create nested serializers
* Build custom API views
* Handle API authentication
* Add permissions to API views
* Create a custom permission
* Implement viewsets and routers
* Use the Requests library to consume the API 

The DRF chapter is very straight-forward and perhaps makes less sense unless we "consume" this API with another client, which is what Antonio demonstrates.  This can be commonly encountered in other backend programs or with AJAX calls from a frontend.

## Chapter 13 - Channels and ASGI

We conclude with the very advanced topic of Asynchronous programming with [Django Channels](https://channels.readthedocs.io/en/stable/), which, like [DRF](https://www.django-rest-framework.org/), is a third-party package for Django.

The chat server shows how you can start to extend beyond simply rendering templates and making db calls.

There are changes from the Django Channels 2.4 that Antonio uses and the 3.x that is current: https://channels.readthedocs.io/en/stable/releases/3.0.0.html#update-to-asgi-3

One place you'll see this is here:

Antonio's 2.4 code:

``` python
from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer),
]
```

Updated for 3.x:

``` python
from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    # if using the django channels 3.x, the below code has to be changed: 
    # https://channels.readthedocs.io/en/stable/releases/3.0.0.html#update-to-asgi-3
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]
```
Recall also that the last mile for this app requires [Redis](https://redis.io/).

Also, again, this is easiest in the following cases:
* when the app is deployed to the VPS
* when your desktop/development machine uses a Mac or Linux OS
* when you are using Windows 10 and WSL

[Running on Windows is not impossible](https://github.com/microsoftarchive/redis), but [Redis isn't really supported by Microsoft](https://github.com/microsoftarchive/redis) in any case.

[Memurai](https://www.memurai.com/) is an alternative as well, but may not work with Antonio's code. That said, the Memurai team [does discuss windows installations](https://www.memurai.com/blog/install-redis-windows-alternatives-such-as-memurai).

Redis is a very common memory key-value store used for caching, so it is eventually worth working with.

# Deployment - Antonio's Strategy and Mine

## Chapter 14 - Deployment

Finally, Antonio covers deployment, which is vital to getting your project onto the web and into the "hands" of your users.

Topics include:

* Configuring your VPS to serve as your production environment
* Understanding [PaaS](https://en.wikipedia.org/wiki/Platform_as_a_service) options.
* Creating custom middleware
* Creating custom management controls for deployment

## Managing settings

Antonio covers the need to manage settings differently depending on what stage of development your application is at.  As such, we establish different settings files to be used conditionally depending on the current environment:

* Development/Local
* Production (deployed to VPS)

take note that when you use this settings approach, you can always use the `--settings` switch for the `manage.py` command:

`manage.py runserver --settings=educa.settings.local`

### uWSGI vs Gunicorn

While I believe Antonio has provided us with a very strong guide, Windows is an afterthough in most of his instructions.  While [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) is likely more performant, we'll stick to [Gunicorn](https://gunicorn.org/) as it is implemented in Python.

### nginx

Arguably the most performant HTTP server available, we'll use [nginx](https://nginx.org/en/docs/) soley on the VPS in deployment.

At this stage, while we will do all of the things Antonio shows in this chapter, we'll do them differently and with a VPS orientation:

1. We'll use Gunicorn
2. We'll configure Nginx on our server (VPS)
3. We'll configure Nginx using the "sites-available" system rather than directly into `nginx.conf`
4. We'll demonstrate both using nginx for static content and [WhiteNoise](https://pypi.org/project/whitenoise/)
5. We'll use [Lets Encrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04) for our SSL work directly on the VPS.
