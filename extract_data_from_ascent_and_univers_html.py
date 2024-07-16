#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 02:17:28 2022

help from these sites
https://towardsdatascience.com/a-guide-to-scraping-html-tables-with-pandas-and-beautifulsoup-7fc24c331cf7
https://www.geeksforgeeks.org/how-to-get-cell-value-from-pandas-dataframe/
https://datagy.io/append-to-lists-python/
https://stackoverflow.com/questions/33704124/using-not-equal-and-nan-together-in-python

Note that the univers data has outdated sales history and that the sales histories don't always have the newest sale listed first'

@author: noah
"""
import bs4
import pandas
import csv
import os


def main():
    # first pull in the ascent data that has the most recent sales information. Univers is out of date!
    # https://realpython.com/python-csv/
    # https://realpython.com/python-ordereddict/
    # https://stackoverflow.com/questions/71524959/python3-calling-csv-dictreader-object-is-not-callable
    ascentData = []
    with open('./data/Neighborhood_Sales.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            ascentData.append(row)
    # print(ascentData)

    combinedData = []
    for i in range(len(ascentData)):
        LongParcelID = ascentData[i]["ParcelNumber"]
        ShortParcelID = LongParcelID[4:]
        extract = {
            "AscentID": ShortParcelID,
            "SiteAddress": ascentData[i]["SiteAddress"],
            "SaleDate": ascentData[i]["RecordedDate"],
            "SalePrice": ascentData[i]["ConsiderationAmount"],
            "AssessmentYear": ascentData[i]["AssessmentYear"],
            "LandValue": ascentData[i]["LandValue"],
            "BuildingValue": ascentData[i]["ImprovementValue"]
        }
        combinedData.append(extract)
        # print(combinedData)

        # open the html file for the ith dictionary
        html_file = ascentData[i]["ParcelNumber"] + "_" + ascentData[i]["SiteAddress"] + ".html"
        with open(f"data/{html_file}", 'r') as f:
            soup = bs4.BeautifulSoup(f, features='html.parser')
        tables = soup.find_all('table')
        tableString = ""
        for j in tables:
            tableString += str(j)
        dataFrames = pandas.read_html(tableString)  # passing literals is deprecated
        # frameCount = len(dataFrames)

        # print(combinedData)
        # add info to the ith dictionary
        # adding info to list of dictionaries: https://www.askpython.com/python/list/list-of-dictionaries
        combinedData[i]["UniversID"] = dataFrames[3].iat[2, 0]

        # dwelling info has 39 rows, 1/2 are empty append programatically
        for j in range(1, len(dataFrames[8])):
            if str(dataFrames[8].iat[j, 1]) != "nan":
                combinedData[i][dataFrames[8].iat[j, 0]] = dataFrames[8].iat[j, 1]
        # print(dataRow)

    # write the csv file, acc. to https://devenum.com/how-to-write-list-of-dictionaries-to-csv-in-python/
    # TODO: deduplicate the dictionary and keep the most informative entries
    highest_key_count = 0
    index = 0
    for i in range(len(combinedData)):
        if (d_len := len(combinedData[i].keys())) < highest_key_count:
            highest_key_count = d_len
            index = i
    with open("./data/ascent_and_univers_data.csv", "a") as ascentUniversData:
        csvwriter = csv.DictWriter(ascentUniversData, combinedData[index].keys(), extrasaction='ignore')
        csvwriter.writeheader()
        csvwriter.writerows(combinedData)


if __name__ == "__main__":
    main()
