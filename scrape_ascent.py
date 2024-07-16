#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:03:12 2022
based on explanations and examples from here:
http://www.compciv.org/guides/python/how-tos/creating-proper-url-query-strings/
https://www.freecodecamp.org/news/how-to-interact-with-web-services-using-python/

alt method was to drive the browser via selenium
https://thenextweb.com/news/how-to-use-python-and-selenium-to-scrape-websites
@author: noah
"""

import requests
import json
import csv

BASE_URL = 'https://ascent.racinecounty.com/'

session = requests.Session()
session.get('https://ascent.racinecounty.com/LandRecords/PropertyListing/RealEstateTaxParcel#/Search')
session.get('https://ascent.racinecounty.com/LandRecords/PropertyListing/SalesHistoryReport')

# Caledonia district ID is 609
# Date is M/D/YYYY, no zeroes required for single digit days and months
# do the first search to find out the total number of records we want to request-value is at the end of the results
query_params = {
    "page": 1,
    "districtId": 609,
    "startDate": "1/1/2021",
    "endDate": "7/30/2022",
    "sortBy": "SITE_ADDR",
    "recordCount": 10
}

query_headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "ascent.racinecounty.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://ascent.racinecounty.com/LandRecords/PropertyListing/SalesHistoryReport",
    "Connection": "keep-alive"
}


def find_number_of_sales():
    query1 = requests.get(f"{BASE_URL}/LandRecords/api/SalesHistoryService", params=query_params,
                          cookies=session.cookies,
                          headers=query_headers)

    # The NumRecord gives an integer, which I checked with type(NumberSales)
    NumberSales = query1.json()['NumRecords']
    return NumberSales


def get_all_data(NumberSales):
    # now update the record count so we can grab all the sales of interest
    # https://www.askpython.com/python/dictionary/how-to-update-a-python-dictionary
    query_params["recordCount"] = str(NumberSales)

    # make the updated query to get all the sales in one json file
    query2 = requests.get(f"{BASE_URL}/LandRecords/api/SalesHistoryService", params=query_params,
                          cookies=session.cookies,
                          headers=query_headers)
    return query2


def write_csv(query2, NumberSales):
    # write the json data to CSV file for manipulation
    # https://www.codespeedy.com/convert-json-to-csv-in-python/
    # https://stackoverflow.com/questions/54002058/how-to-convert-json-to-csv-in-python
    with open("./data/ascent_data.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(query2.json()["Results"][0].keys())
        for i in range(NumberSales):
            writer.writerow(query2.json()["Results"][i].values())


def write_json(query2):
    # write the data to json file for later use
    with open("./data/ascent_data.json", 'w') as jsonFile:
        jsonString = json.dumps(query2.json())
        jsonFile.write(jsonString)


def main():
    numSales = find_number_of_sales()
    data = get_all_data(numSales)
    write_csv(data, numSales)
    write_json(data)


if __name__ == "__main__":
    main()
