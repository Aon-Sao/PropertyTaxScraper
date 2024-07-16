#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 00:03:24 2022
scrape the univers site for details about neighborhood sales

@author: noah
"""
import csv
import requests


def main():
    # taken from https://stackoverflow.com/questions/48716446/python-skip-header-row-with-csv-reader
    with open("./data/Neighborhood_Sales.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # strip off first 4 characters for compatibility with the univers site
            # https://datagy.io/python-remove-first-n-characters-from-string/
            LongParcelNumber = row['ParcelNumber']
            ShortParcelNumber = LongParcelNumber[4:]
            print(ShortParcelNumber)
            query = requests.get(
                "http://www.caledonia.univers-clt.com/view_property_R.php?account_no=" + ShortParcelNumber + "&series_card=1")
            print(query)
            # https://www.easytweaks.com/python-write-to-text-file/
            # write file names with long parcel number to ease compatibility when merging data from Ascent and Univers files
            with open("./data/" + LongParcelNumber + "_" + row["SiteAddress"] + ".html", mode="w") as f:
                f.write(query.text)


if __name__ == "__main__":
    main()
