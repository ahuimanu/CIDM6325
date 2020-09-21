import csv
import json
import os

from pathlib import Path

# will hold records for processing
records = []
counter = 0

class MarketDataRecord:
    def __init__(self, id, passengers, freight, mail, distance, carrier_id, \
        carrier_name, orig_airport_id, orig_iata_code, \
        orig_city_name, orig_state_abr, dest_airport_id, \
        dest_iata_code, dest_city_name, dest_state_abr, month):

        self.id = id
        self.passengers = passengers
        self.freight = freight
        self.mail = mail
        self.distance = distance
        self.carrier_id = carrier_id
        self.carrier_name = carrier_name
        self.orig_airport_id = orig_airport_id
        self.orig_iata_code = orig_iata_code
        self.orig_city_name = orig_city_name
        self.orig_state_abr = orig_state_abr
        self.dest_airport_id = dest_airport_id
        self.dest_iata_code = dest_iata_code
        self.dest_city_name = dest_city_name
        self.dest_state_abr = dest_state_abr
        self.month = month

    def django_json_serialize(self, modelname):
        """
        output python tuple as json.  See https://docs.python.org/3/library/json.html
        """

        outdata = {
            "model": modelname,
            "pk": self.id,
            "fields": {
                "passengers": self.passengers,
                "freight": self.freight,
                "mail": self.mail,
                "distance": self.distance,
                "carrier_id": self.carrier_id,
                "carrier_name": self.carrier_name,
                "orig_airport_id": self.orig_airport_id,
                "orig_iata_code": self.orig_iata_code,
                "orig_city_name": self.orig_city_name,
                "orig_state_abr": self.orig_state_abr,
                "dest_airport_id": self.dest_airport_id,
                "dest_iata_code": self.dest_iata_code,
                "dest_city_name": self.dest_city_name,
                "dest_state_abr": self.dest_state_abr,
                "month": self.month,
            }
        }

        return outdata


def parse_line(record):
    """
    split a line from the infile into parts to create a MarketDataRecord
    """

    # make sure we use the script-level counter
    global counter

    if len(record) == 15:
        aid = counter
        counter += 1

        return MarketDataRecord(aid,         #id
                                record[0],    # passengers
                                record[1],    # freight
                                record[2],    # mail
                                record[3],    # distance
                                record[4],    # carrier_id
                                record[5],    # carrier_name
                                record[6],    # orig_airport_id
                                record[7],    # orig_iata_code
                                record[8],    # orig_city_name
                                record[9],    # orig_state_abr
                                record[10],   # dest_airport_id
                                record[11],   # dest_iata_code
                                record[12],   # dest_city_name
                                record[13],   # dest_state_abr                                
                                record[14],)  # month
    else:
        return None


def parse_data_to_json_list(infile, modelname):
    """ 
    read CSV file using the CSV library:
    https://docs.python.org/3/library/csv.html?highlight=csv
    Note: A Path object has an open method: 
    https://docs.python.org/3/library/pathlib.html#pathlib.WindowsPath
    """

    # make sure we use the script-level records
    global records

    # from the csv Python library
    with infile.open("r") as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel', delimiter=',', quotechar='"')
        for row in csvreader:
            records.append(parse_line(row).django_json_serialize(modelname))


def write_data_to_django_fixture(outfile):
    """ 
    Write json file in the Django serialization form
    Note: A Path object has an open method: 
    https://docs.python.org/3/library/pathlib.html#pathlib.WindowsPath
    """    
    json.dump(records, outfile.open("w"))


def main():

    infilename = '921058182_T_T100D_MARKET_US_CARRIER_ONLY.csv'
    infilepath = Path(__file__).resolve().parent.joinpath('data/').joinpath(infilename)
    outfilename = 'marketdata.json'
    outfilepath = Path(__file__).resolve().parent.joinpath('data/').joinpath(outfilename)

    modelname = "air_carrier_market_data.MarketData"    

    print('Reading T-100 CSV file')    
    parse_data_to_json_list(infilepath, modelname)
    print("writing json to django serialization format")
    write_data_to_django_fixture(outfilepath)


# explaination of why this is here: https://realpython.com/python-main-function/
if __name__ == "__main__":
    main()

