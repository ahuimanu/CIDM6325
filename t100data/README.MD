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