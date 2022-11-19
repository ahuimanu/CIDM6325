# CIDM6325 - Fall 2022

## General Notes
* [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator)

* Commands to run when checking for outdated packages in your Virtual Environment
    * Be sure that your VE is activated (`source .venv/Scripts/activate`)
    * check for outdated packages `python -m pip --outdated`
    * update package(s) as appropriate `python -m pip install --upgrade <name-of-package>`

## Candidate Heroku Replacements
* render.io
* python anywhere
* Fly.io

## Django for Beginners - [Book Website](https://djangoforbeginners.com/)
### Chapter 1 Steps
1. Create virtual environment on windows: `python -m venv .venv`
2. Create new project
3. Run the project
4. Create git repository: `git init`

Django Secret Key Generator: https://django-secret-key-generator.netlify.app/

### Chapter 4

Variations to the steps:
1. `cd onedrive\desktop\code`
1. `mkdir message-board`
1. `cd message-board`
1. `python -m venv .venv` (may not be needed if you are using the same VE for all projects in the book)
1. `.venv\Scripts\Activate.ps1` (or in git-bash: `source .venv/Scripts/activate`)
1. `python -m pip install django~=4.0.0`
1. `django-admin startproject django_project .`
1. `python manage.py startapp posts`

### Chapter 5 Blog App

Note that I'm making a new subdirectory for each chapter/app from the book.  This is some what of a departure from how Will Vincent has organized things.


This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

## Guide to Book Topics for Final Project (Baseline, Good, Better, Best)

I have classified the learning objectives from Antonio's book according to the following scheme.  Each category is relative to the following requirements for your final project:

* You must implement *all* **Baseline** components - Gets you to 70% of the value
* You will implement *at least* six **Good** components - Gets you to 80% of the vaue
* You will implement *at least* two **Better** components - Gets you to 85% of the value
* You will implement *at least* two **Best** components - Gets you to 90% of the value

Where is the remaining 10%? It comes from the synthesis and service to your idea (implementation).

* **Baseline**: Essential Django knowledge that must be demonstrated in your final project
* **Good**: Fundamental knowledge that sets up a more useful app
* **Better**: Approaching a higher degree of robustness
* **Best**: Approaching professional-grade features and tools

Topic                                   | Baseline  | Good  | Better  | Best
---                                     | ---       | ---   | ---     | ---
***Chapter 3***                         |           |       |         |
Templates                               | x         |       |         |
Template Inheritance                    | x         |       |         |
Views                                   | x         |       |         |
Class-Based Views                       | x         |       |         |
URLs                                    | x         |       |         |
Routing                                 | x         |       |         |
***Chapter 4***                         |           |       |         |
Model Classes                           | x         |       |         |
Django Admin configuration              | x         |       |         |
Tests                                   |           | x     |         |
***Chapter 5***                         |           |       |         | 
Static Files                            | x         |       |         |
Queries                                 | x         |       |         |
***Chapter 6***                         |           |       |         |
Class-Based Forms                       | x         |       |         |
***Chapter 7***                         |           |       |         |
Authentication                          | x         |       |         |
Social auth integration                 |           | x     |         |
Postgres                                |           | x     |         |
***Chapter 8***                         |           |       |         |
Custom user models                      |           | x     |         |
Ad hoc forms                            |           | x     |         |
***Chapter 10***                        |           |       |         |
Bootstrap                               | x         |       |         |
***Chapter 11***                        |           |       |         |
Custom templates                        |           | x     |         |
Account management                      |           | x     |         |
***Chapter12***                         |           |       |         |
Email                                   |           | x     |         |
***Chapter 13***                        |           |       |         |
django_crispy_forms                     |           | x     |         |
***Chapter 14***                        |           |       |         | 
authorization                           |           | x     |         |
CBV mixins                              |           | x     |         |
***Chapter15***                         |           |       |         |
ManytoMany relationships                |           | x     |         |
***Chapter16***                         |           |       |         |
heroku deployment                       |           |       | x       |
vps deployment (nginx, gunicorn)        |           |       | x       |
Static assets with nginx and whitenoise |           | x     |         |
Securing with SSL                       | x         |       |         |
Custom middlewre                        |           |       | x       |
Task scheduling with cron               |           | x     | x       |
CI/CD with Github                       |           |       |         | x
***3rd Party***                         |           |       |         |
[Django admin](https://github.com/wsvincent/awesome-django#admin) | | | | x
[APIs](https://github.com/wsvincent/awesome-django#apis) | |  |         | x
[Async](https://github.com/wsvincent/awesome-django#async) |           |       |         | x
[ECommerce](https://github.com/wsvincent/awesome-django#ecommerce) |    |   |   | x
[Files and Images](https://github.com/wsvincent/awesome-django#filesimages) |    |   |   | x
[Model enhancements](https://github.com/wsvincent/awesome-django#models) |   |   |   | x
[Search](https://github.com/wsvincent/awesome-django#search) |   |   |   | x
[Tasks and Job Scheduling](https://github.com/wsvincent/awesome-django#task-queues) |   |   |   | x
[Users and SSO](https://github.com/wsvincent/awesome-django#users) |   |   |   | x
[Views](https://github.com/wsvincent/awesome-django#views) |   |   |   | x
