# Code Repository for CIDM6325

## Fall 2020

We will work through Antonio Melé's [Django By Example - Third Edition](https://www.packtpub.com/web-development/django-3-by-example-third-edition) Applications Together:

* [Part 1 - Building a Blog](https://github.com/ahuimanu/CIDM6325/tree/master/blog)
* [Part 2 - Building a Social Website](https://github.com/ahuimanu/CIDM6325/tree/master/bookmarks)
* Part 3 - Building an Online Shop (eCommerce)
* Part 4 - Building a Chat Server using an API

I encourage you to hand-code from the book and resist the temptation to just copy and paste from the source files.

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

## Python Tips and Guidance

I will keep some general Python notes here:
* For [Visual Studio Code](https://code.visualstudio.com/), please use the [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
* The Python Extension should help you to adhere to the [Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) with its [linting](https://en.wikipedia.org/wiki/Lint_(software)) capabilities.

## Build a Blog Notes

Here are observations and notes from the chapters

### Chapter 1 - Build a Blog

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

#### Models

With `Django` you are persisting business data using [Object/Relational Mapping](https://en.wikipedia.org/wiki/Object-relational_mapping), which is a fairly standard approach to web application development.

This is there to structure your database.  Django Models are classes.  Review the basic structures and provisions of the [Python language](https://www.w3schools.com/python/default.asp).

#### Admin

A great feature of Django is the built-in admin interface - you can perform CRUD operations here.

#### Queries

There is a built-in query expression structure that saves time and avoids the need to write SQL directly in most cases.

#### Views

We will try to use Class-Based-Views as much as possible.  However, Function-Based-Views are also possible.

#### Secret Key

Django uses a SECRET_KEY for many security purposes in your project.  Since I will be encouraging the use of Github, publishing your secret key is a problem to avoid.  In fact, if you look at this repository, the initial commit contains a secret key (since changed).

Relevant part of the documentation: [The secret key must be a large random value and it must be kept secret.](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/#secret-key)

Also, since we'll use Git and Github, placing an effective GITIGNORE file into our repository is important: [Gitignore for a Django project](https://djangowaves.com/tips-tricks/gitignore-for-a-django-project/)

#### Templates

Templates are HTML files with escapes to contain minimal display and presentation logic.  The _beauty_ of your pages will completely rely on one of a few options:
* Your skill with CSS
* Use of a robust component library
* Some template you find/purchase

### Chapter 2 - Enhancing Your Blog with Advanced Features

---

Antonio really adds in some useful features here and provides a fairly advanced use of Django within two chapters of the book:
* Email
* Comments
* Tags and metadata
* Recommendations

#### Forms and Email

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

#### Comments and Tags

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

### Chapter 3 - Extending the Blog Application

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