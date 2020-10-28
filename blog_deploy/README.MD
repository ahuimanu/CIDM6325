# Blog Template and Deployment

This project has been created in support of Assignment 7.5, centering on deployment.

A significant part of this tutorial is based on [How To Set Up Django with Postgres, Nginx, and Gunicorn on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04), written by [Erin Glass](https://www.digitalocean.com/community/users/eglass).

Showing some steps on:
* how to select a [Bootstrap 4](https://getbootstrap.com/) [template](https://startbootstrap.com/templates/blog-home)
* steps for deployment

## Preparing for Deployment

For our purposes here, the first three steps in Erin's tutorial should be followed again for a new database and database user:

* [Installing the Packages from the Ubuntu Repositories](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04#installing-the-packages-from-the-ubuntu-repositories)
* [Creating the PostgreSQL Database and User](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04#creating-the-postgresql-database-and-user)
* [Creating a Python Virtual Environment for your Project](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04#creating-a-python-virtual-environment-for-your-project)

However, we do not need to start a new django project as we have one in source control.  However, it would be best if the project were located outside of a combined repository.  Either way will work, however.

## Ensuring our domain name is associated with our servers

In Digital Ocean's cloud dashboard, you go to networking and associate your domain with your droplet.  At your domain registrar, you provide the nameserver information.

## Ensuring nginx is set for TLS/SSL

We also need to ensure that Nginx is set to go with Let's Encrypt prior to the Gunicorn work with Django:

* [How To Install Nginx on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04)
* [How To Secure Nginx with Let's Encrypt on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04)