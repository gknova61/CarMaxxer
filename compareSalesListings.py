#!/usr/bin/env python3

"""compareSalesListings.py: Compares two sales listings CSV files from different times and exports 'sales' to CSV file"""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com "

import lib.csvHandler as csv
import lib.ioHandler as io
import logging
import os
import shutil

logging.basicConfig(filename='carmax-sales-data.log',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

currentSalesListingsFilename = "salesListingsCurrent.csv"
pastSalesListingsFilename = "salesListingsPast.csv"
newSalesFilename = "newSales.csv"

def checkForListingData():
    if not os.path.exists(pastSalesListingsFilename):
        if os.path.exists(currentSalesListingsFilename):
            shutil.copyfile(currentSalesListingsFilename, pastSalesListingsFilename)
            print("No past listings data found, copied current to past")
            logging.info("No past listings data found, copied current to past")
        else:
            print("Error: No listing data found")
            print("Please run listingScraper to get a list of vehicles from CarMax")
            logging.error("No listing data found")
            logging.info("FAILED compareSalesListings")
            exit(1)

    if not os.path.exists(currentSalesListingsFilename):
        print("Error: No current listing data found")
        print("Please run listingScraper to get a list of vehicles from CarMax")
        logging.error("No current listing data found")
        logging.info("FAILED compareSalesListings")
        exit(1)

#region Search List Functions
def buildSearchIndex(listToIndex, colNamesToBuildOn):
    searchIndex = {}

    for index,row in enumerate(listToIndex):
        fullSearchTerm = ''
        for colName in colNamesToBuildOn:
            fullSearchTerm += row[colName]
        searchIndex[fullSearchTerm] = index

    return searchIndex

def search(listToSearch,searchIndex,keyword):
    searchResult = {}
    try:
        searchResult = listToSearch[searchIndex[keyword]]
    except:
        return False

    return searchResult
#endregion

logging.info("STARTED compareSalesListings")

print("Checking for listing data from CarMax...")
checkForListingData()

#region Prepare listing data for comparison
print("Importing CSVs containing listing data of used car sales...")
pastSalesListings = csv.importCSV(pastSalesListingsFilename)
currentSalesListings = csv.importCSV(currentSalesListingsFilename)

print("Building search index based on VIN and Stock Number...")
pastSalesListingsIndex = buildSearchIndex(pastSalesListings,['stockNumber','vin'])
currentSalesListingsIndex = buildSearchIndex(currentSalesListings,['stockNumber','vin'])
#endregion

#region Compare Listing data from past and present to find vehicle sales
soldCars = []
newListings = []

for vehicle in pastSalesListings:
    vehicleIdentifier = vehicle['stockNumber'] + vehicle['vin']
    if not search(currentSalesListings,currentSalesListingsIndex,vehicleIdentifier):
        soldCars.append(vehicle)

for vehicle in currentSalesListings:
    vehicleIdentifier = vehicle['stockNumber'] + vehicle['vin']
    if not search(pastSalesListings,pastSalesListingsIndex,vehicleIdentifier):
        newListings.append(vehicle)
#endregion to fin

#region Export new sales CSV and rename present to past for next run
csv.exportCSV(newSalesFilename, soldCars)
io.rename(currentSalesListingsFilename,pastSalesListingsFilename)
#endregion

logging.info("SUCCESS compareSalesListings")