# CIDM6325 - Fall 2022

## General Notes
* [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator)

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