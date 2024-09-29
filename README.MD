# CIDM6325 - Fall 2024 #
README Outline:

- A [Git Cheat Sheet](https://training.github.com/downloads/github-git-cheat-sheet/) is available as a quick reference for common `git` commands.
- Boostrap Crash Course (freecodecamp): [Full Bootstrap 5 Tutorial for Beginners](https://www.freecodecamp.org/news/full-bootstrap-5-tutorial-for-beginners/)

## Video Notes ##
- Overall tools and techniques - Video 1
- Emails and Email Backends - Video 2
- Docker and Postgres - Video 3
- Social SSO - Video 4

## SendGrid and Anymail
Steps from https://anymail.dev/en/v12.0/esps/sendgrid/
1. `pip install "django-anymail[sendgrid]"
2. add `anymail` to INSTALLED_APPS

[back to outline](#cidm6325---fall-2024)

# Docker Stuff
WSL2 is probably the best option for Windows.
![WSL2](./img/docker_install_dialog.png)

You can use the shell from within the Docker Interface
![Docker Interface](./img/docker_interface2.png)

Or, if on Windows, use PowerShell. If on Mac, Terminal is fine.
![PowerShell](./img/PowerShell.png)

## General Notes ##
* [The Django Secret Key Generator](https://django-secret-key-generator.netlify.app/) - [Source Code for the curious](https://github.com/RealOrangeOne/django-secret-key-generator)

* Commands to run when checking for outdated packages in your Virtual Environment (VE):
    * Be sure that your VE is activated (`source .venv/Scripts/activate`)
    * check for outdated packages `python -m pip --outdated`
    * update package(s) as appropriate `python -m pip install --upgrade <name-of-package>`

In addition to the book, this is a good resource: [W3Schools Django](https://www.w3schools.com/django/index.php)

[back to outline](#cidm6325---fall-2024)

## Miscellaneous Notes ##
- **Templates and Bootstrap** - I will strongly recommend that you use and develop familiarity with [Bootstrap](https://getbootstrap.com/) as a CSS framework for all of your work in this class.
- **Classy Class-Based Views** - Should you wish to go in this direction: [https://ccbv.co.uk/](https://ccbv.co.uk/)
- **Environment Variables** - I have used [python-dotenv](https://pypi.org/project/python-dotenv/) forever and have done so in my code - Antonio uses [python-decouple](https://pypi.org/project/python-decouple/).
- **Candidate Heroku Replacements** - Heroku used to be the best free Django deployment platform - it is no longer free.  Here are some replacement services.
    * render.io
    * python anywhere
    * Fly.io
    * [Railway](https://railway.app/)

This README file is constructed using [MarkDown](https://www.markdownguide.org/basic-syntax).  Here is another good [Markdown reference](https://commonmark.org/help/).

[back to outline](#cidm6325---fall-2024)
