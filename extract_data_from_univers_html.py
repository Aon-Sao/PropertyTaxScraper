#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 02:17:28 2022

help from these sites
https://towardsdatascience.com/a-guide-to-scraping-html-tables-with-pandas-and-beautifulsoup-7fc24c331cf7
https://www.geeksforgeeks.org/how-to-get-cell-value-from-pandas-dataframe/
https://datagy.io/append-to-lists-python/
https://stackoverflow.com/questions/33704124/using-not-equal-and-nan-together-in-python

@author: noah
"""

import pandas
import csv
import os


def main():
    dataFrames = pandas.read_html("./data/042233049001_10019 DUNKELOW RD.html")

    frameCount = len(dataFrames)
    print(frameCount)

    # print(dataFrames[3])

    # build the header row for writing the csv file
    headerRow = [dataFrames[3].iat[1, 0], dataFrames[3].iat[1, 3], "Land Valuation", "Building Valuation",
                 "Total Valuation", "Sale Date", "Sale Price", "Sale Type"]
    # print(headerRow)

    # dwelling info has 39 rows, 1/2 are empty append programatically
    for i in range(1, len(dataFrames[8])):
        if str(dataFrames[8].iat[i, 0]) != "nan":
            headerRow.append(dataFrames[8].iat[i, 0])
    # print(headerRow)

    # write header to file
    with open("./data/univers_data.csv", "a") as universData:
        # creating writer object
        csv_writer = csv.writer(universData)
        # appending data
        csv_writer.writerow(headerRow)

    # loop through all the univers html files to pull data and write to csv file

    with os.scandir(".") as it:
        for entry in it:
            if entry.name.endswith(".html") and entry.is_file():
                print(entry.path)
                dataFrames = pandas.read_html(entry.path)
                frameCount = len(dataFrames)
                print(frameCount)

                # build the data row for writing the csv file
                dataRow = [dataFrames[3].iat[2, 0], dataFrames[3].iat[2, 3], dataFrames[9].iat[1, 1],
                           dataFrames[9].iat[3, 1], dataFrames[9].iat[5, 1], dataFrames[11].iat[3, 1],
                           dataFrames[11].iat[3, 2], dataFrames[11].iat[3, 3]]
                # print(dataRow)

                # dwelling info has 39 rows, 1/2 are empty append programatically
                for i in range(1, len(dataFrames[8])):
                    if str(dataFrames[8].iat[i, 1]) != "nan":
                        dataRow.append(dataFrames[8].iat[i, 1])
                # print(dataRow)

                with open("./data/univers_data.csv", "a") as universData:
                    # creating writer object
                    csv_writer = csv.writer(universData)
                    # appending data
                    csv_writer.writerow(dataRow)


if __name__ == "__main__":
    main()
