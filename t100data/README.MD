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


## Queries for you to complete

I will have demonstrated one or two queries, but the full list to attempt is:

* What are the top 5 airports in terms of:
    * Total passengers by origin
    * Total passengers by destination
* What are the top 5 airports in terms of:
    * Total freight by origin
    * Total freight by destination
* What are the top 5 airports in terms of:
    * Total mail by origin
    * Total mail by destination
* What are the top 5 airports in terms of:
    * Total distance by origin
    * Total distance by destination    
* Which airport reported the most passengers by month?
* Which airport reported the longest distance by month?
* Which airline reported the most freight carried?
* Which airline reported the most passengers carried?
* Which airline reported the most mail carried?
* Which airline reported the longest flight distance?
* Rank order passengers carried, by month, for these airlines:
    * AA (American Airlines)
    * AS (Alaska Airlines)
    * DL (Delta Airlines)
    * UA (United Airlines)
    * WN (Southwest Airlines)
* Find the average number of passengers for flights into:
    * LAX (Los Angeles)
    * SFO (San Francisco)
    * DFW (Dallas-Fort Worth)
    * ATL (Atlanta)
    * ORD (Chicago)
* Find the average volume of freight for flights departing:
    * MIA (Miami)
    * MEM (Memphis)
    * JFK (New York JFK)
    * ANC (Anchorage)
    * SDF (Louisville)
* What city pairs represent the most freight carried for the longest distance?
* What city pairs represent the most mail carried for the shortest distance?

## Queries

Answering these questions provides you with an opportunity to practice and perfect your grasp and command of [Django ORM provisions for querying](https://docs.djangoproject.com/en/3.1/topics/db/queries/).  Some key aspects to study:

* [QuerySets and functions](https://docs.djangoproject.com/en/3.1/topics/db/queries/)
* [Q Objects](https://docs.djangoproject.com/en/3.1/topics/db/queries/#complex-lookups-with-q-objects) for complex lookups
* [Relationships](https://docs.djangoproject.com/en/3.1/topics/db/queries/#related-objects)
* [Aggregations](https://docs.djangoproject.com/en/3.1/topics/db/aggregation/)
* [Basic Search](https://docs.djangoproject.com/en/3.1/topics/db/aggregation/)

## Views, CBVs, and Templates

For each query above, create a view so that each can be answered by simply following a link.  Also, use (as much as possible), the following [Class-Based Views](https://ccbv.co.uk/) for the UI:
* [TemplateView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.base/TemplateView/): For basic pages
* [ListView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.list/ListView/): To show lists of output
* [DetailView](https://ccbv.co.uk/projects/Django/3.0/django.views.generic.detail/DetailView/): To show the details of any given record