# T-100 Data Loading

This project extends our knowledge from Antonio Mele's book by considering how we might obtain and pre-load data.  Not all data of interest is generated from direct interaction and often a Django front-end is useful for accessing other data, such as regular reports.

## ETL Extraction, Transformation, and Loading

The issue is that you often have a few options for loading data for availability in your Django APP:

* Direct database dumps (using pgadmin4 for instance) - [Pgadmin Backup and Restore](https://www.pgadmin.org/docs/pgadmin4/development/backup_and_restore.html)
* Consuming some serialization of objects/data - [Django Fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/)
* Direct flat-file reading - [Python File Handling](https://www.w3schools.com/python/python_file_handling.asp)
* Accessing data from API calls (REST call usually) - [Requests](https://pypi.org/project/requests/)

## CBV [Class-Based Views](https://ccbv.co.uk/)

We can get a fairly simple list view and detail view with built-in [Django Class-Based Views](https://docs.djangoproject.com/en/3.1/topics/class-based-views/).

## [United States Department of Transportation - Bureau of Transportation Statistics](https://www.bts.gov/)

The BTS provides statistics on US and International Air Carriers in a database called The T-100.  Specifically, I will focus on the [Air Carriers : T-100 Domestic Market (U.S. Carriers)](https://www.transtats.bts.gov/Fields.asp) Tables.

## Procedure

1. ***Understand the Data***: Our first order of business will be to review and understand the [Air Carriers : T-100 Domestic Market (U.S. Carriers)](https://www.transtats.bts.gov/Fields.asp).  


1. ***Develop Models***: From the description of the views, it should be possible to develop appropriate [Django Models](https://docs.djangoproject.com/en/3.1/topics/db/models/).

1. ***Create new project and virtual environment*** - As we've done previously, use [django-admin](https://docs.djangoproject.com/en/3.1/ref/django-admin/) and either [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).  Note, stick to venv if you've been having trouble with Conda.

1. ***Create an ETL Process*** [Transform](https://en.wikipedia.org/wiki/Data_transformation) the [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) data downloaded from the [Air Carriers : T-100 Domestic Market (U.S. Carriers)](https://www.transtats.bts.gov/Fields.asp) Tables into importable serializations using [Django Fixtures](https://docs.djangoproject.com/en/3.1/howto/initial-data/).  *NOTE*: I will have included code for this in the [Github Repo for the course](https://github.com/ahuimanu/CIDM6325).

1. ***Autoload Fixtures***: Create a `fixtures` folder in your project so that Django will auto-load your ETL data.

1. ***Develop Queries***: This will eventually be an assignment where I direct you to develop a number of queries so that you are confortable with [Django as a web application framework](https://docs.djangoproject.com/en/3.1/misc/design-philosophies/) that is useful for accessing data and data inquiries.

1. ***List/Detail CBVs***: Use the [ListView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/) and [DetailView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/) [CBVs](https://ccbv.co.uk/) to show the results of various queries of the [Air Carriers : T-100 Domestic Market (U.S. Carriers)](https://www.transtats.bts.gov/Fields.asp) data.