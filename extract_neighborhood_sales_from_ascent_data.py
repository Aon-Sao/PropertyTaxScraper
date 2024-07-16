#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 22:10:54 2022

@author: noah
"""
import json
import csv


def main():
    with open("./data/ascent_data.json", "r") as rf:
        query2 = json.load(rf)
    # print(query2["Results"][959])
    # print(query2["Results"][959]["SiteAddress"])
    NumberSales = query2["NumRecords"]

    # list of streets around our house
    streets = [
        "Sienna Ct",
        "Debby Ln",
        "Prairie Crossing Dr",
        "Meadow Rose Ct",
        "Scenic Way",
        "Wild Ginger Way",
        "Goldenrod Ln",
        "Perennial Pkwy",
        "Morris St",
        "Button Bush Dr",
        "White Manor Ct",
        "Dana Dr",
        "Monica Dr",
        "Dunkelow Rd",
        "Lynndale Ln",
        "Morgan Ct",
        "Meadow Park Ln"
    ]

    csv_file = open('./data/Neighborhood_Sales.csv', 'w')
    write = csv.writer(csv_file)
    write.writerow(query2["Results"][0].keys())
    for i in range(NumberSales):
        for s in streets:
            #        print(s.lower())
            if s.lower() in query2["Results"][i]["SiteAddress"].lower():
                write.writerow(query2["Results"][i].values())
    csv_file.close()


if __name__ == "__main__":
    main()
