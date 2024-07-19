#!/usr/bin/env python

import io
import bs4
import csv
import json
import pandas
import requests
from config import *


def query_ascent_data():
    """Finds how many sales have been made, retrieves data for all of them,
    and writes it to a single JSON file"""
    session = requests.Session()
    session.get(f'{BASE_URL}/LandRecords/PropertyListing/RealEstateTaxParcel#/Search')
    session.get(f'{BASE_URL}/LandRecords/PropertyListing/SalesHistoryReport')
    query_params = {
        "page": 1,
        "districtID": CALEDONIA_DISTRICT_ID,
        "startDate": START_DATE,
        "endDate": END_DATE,
        "sortBy": "SITE_ADDR",
        "recordCount": 10  # There's probably at least 10
    }
    query_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "ascent.racinecounty.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"{BASE_URL}/LandRecords/PropertyListing/SalesHistoryReport",
        "Connection": "keep-alive"
    }

    def get_number_of_sales():
        """Makes an API call to find the number of sales records
            :return int
        >>> isinstance(get_number_of_sales(), int)  # This is a 'doctest' btw
        True
        """
        url = f"{BASE_URL}/LandRecords/api/SalesHistoryService"
        response = requests.get(url,
                                params=query_params,
                                cookies=session.cookies,
                                headers=query_headers)
        assert response.status_code != 404, f"Got 404 from {url}"
        return response.json()["NumRecords"]

    def get_all_sales(number_of_sales):
        """Makes an API call to get the sales data
            :return json of results"""
        query_params["recordCount"] = number_of_sales
        response = requests.get(f"{BASE_URL}/LandRecords/api/SalesHistoryService",
                                params=query_params,
                                cookies=session.cookies,
                                headers=query_headers)
        return response.json()["Results"]

    def write_json(jsn):
        with open("./data/ascent_data.json", 'w') as fout:
            fout.write(json.dumps(jsn))

    number_of_sales = get_number_of_sales()
    results_json = get_all_sales(number_of_sales)
    write_json(results_json)


def process_ascent_data_to_csv():
    """ascent_data.json -> Neighborhood_Sales.csv
    Extracts the properties of interest per the STREETS constant
    and write the filtered data to a CSV file"""
    with open("./data/ascent_data.json", 'r') as fin:
        jsn = json.load(fin)
        with open("./data/Neighborhood_Sales.csv", 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow(jsn[0].keys())
            for i in jsn:
                for j in STREETS:
                    if j.lower() in i["SiteAddress"].lower():
                        writer.writerow(i.values())


def dict_to_html_filename(d):
    """Small helper function to match a dictionary of property data up with a file name
        :return str"""
    long_parcel_num = d["ParcelNumber"]
    return "./data/" + long_parcel_num + "_" + d["SiteAddress"] + ".html"


def query_univers_data():
    """For each property in the Neighborhood Sales file, query univers for more information
    writing the html response to disk for later use"""
    with open("./data/Neighborhood_Sales.csv", 'r') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            long_parcel_num = row["ParcelNumber"]
            short_parcel_num = long_parcel_num[4:]
            response = requests.get("http://www.caledonia.univers-clt.com/view_property_R.php?account_no="
                                    + short_parcel_num + "&series_card=1")
            with open(dict_to_html_filename(row), 'w') as fout:
                fout.write(response.text)


def process_and_merge_datasets():
    """Read in the Ascent data. Extract the relevant fields from each property as a dict.
    Read the Univers html responses. Process them into a dictionary of data.
    Merge the Ascent dict with the Univers dict for a given property. Append this to a list.
    Write the collected data out to a CSV file."""
    combinedData = list()
    with open("./data/Neighborhood_Sales.csv", 'r') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            ascentData = {
                "AscentID": row["ParcelNumber"][4:],
                "SiteAddress": row["SiteAddress"],
                "SaleDate": row["RecordedDate"],
                "SalePrice": row["ConsiderationAmount"],
                "AssessmentYear": row["AssessmentYear"],
                "LandValue": row["LandValue"],
                "BuildingValue": row["ImprovementValue"]
            }

            with open(dict_to_html_filename(row)) as html_fin:
                soup = bs4.BeautifulSoup(html_fin, features="html.parser")
            tables = soup.find_all("table")
            tableString = ""
            for i in tables:
                tableString += str(i)
            dataFrames = pandas.read_html(io.StringIO(tableString))

            univers_dict = dict()
            univers_dict["UniversID"] = dataFrames[3].iat[2, 0]
            dwelling_info_dataFrame = dataFrames[8]
            iterator = dwelling_info_dataFrame.itertuples()
            next(iterator)  # Skip headers
            for i in iterator:
                if str(i[1]) != "nan":
                    univers_dict[i[1]] = i[2] if str(i[2]) != "nan" else "Unknown"
            merged_dict = ascentData | univers_dict
            combinedData.append(merged_dict)
    with open("./data/ascent_and_univers_data.csv", 'w') as fout:
        writer = csv.DictWriter(fout, combinedData[0].keys())
        writer.writeheader()
        writer.writerows(combinedData)


def main():
    """Call the functions in the correct order"""
    query_univers_data()
    process_ascent_data_to_csv()
    query_univers_data()
    process_and_merge_datasets()


if __name__ == "__main__":
    """If this is the 'main' program being run (as opposed to being imported),
    then execute the main function."""
    main()
