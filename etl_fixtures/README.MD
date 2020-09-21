# ETL to Django Fixture

This is a basic library/program that reads an extract of the [T-100 Domestic Market](https://www.transtats.bts.gov/Tables.asp?DB_ID=110&DB_Name=Air%20Carrier%20Statistics%20%28Form%2041%20Traffic%29-%20%20U.S.%20Carriers&DB_Short_Name=Air%20Carriers) Tables from the [U.S. Department of Transportation - Bureau of Transportation Statistics (BTS) ](https://www.bts.gov/).  The data can be downloaded as a CSV file from the BTS website.

The task is to then convert this data to a [Django Serialization format] for further processing and to provide [initial data for models](https://docs.djangoproject.com/en/3.1/howto/initial-data/).

This code uses the following elements of the python library:

* [CSV](https://docs.python.org/3/library/csv.html) for CSV file reading and writing
* [JSON](https://docs.python.org/3/library/json.html) for JSON encoding and decoding

## Motivation

Among the many reasons for learning about web application development, primary among them is your ability to obtain and share data.  Being able to import data into your [Django Application](https://www.djangoproject.com/) constitutes a key and vital skill.

