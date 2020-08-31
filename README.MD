# Code Repository for CIDM6325

## Fall 2020

We will work through Antonio Melé's [Django By Example - Third Edition](https://www.packtpub.com/web-development/django-3-by-example-third-edition) Applications Together:

* Building a Blog
* Building a Social Website
* Building an Online Shop (eCommerce)
* Building a Chat Server using an API

I encourage you to hand-code from the book and resist the temptation to just copy and paste from the source files.

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

We will also explore using the free tier of services like (SendGrid)[https://sendgrid.com/] or [MailChimp](https://mailchimp.com/)

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