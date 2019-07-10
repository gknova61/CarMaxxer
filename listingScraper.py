#!/usr/bin/env python3

"""salesScraper.py: Pulls data from all CarMax sales listings and exports to a file called salesListingsCurrent.csv."""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com "

import lib.csvHandler as csv
import furl
import logging
import math
import json
import time
from selenium import webdriver

logging.basicConfig(filename='carmax-sales-data.log',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)

baseUrl = "https://www.carmax.com/cars/api/search/run"
params = {"uri": "/cars?price=200000","skip": 0,"take": 1000, "radius": 250000, "zipCode": 94014, "sort": 20}

exportCSVFilename = 'salesListingsCurrent.csv'

def constructUrl():
    global baseUrl
    global params

    f = furl.furl(baseUrl)
    f.args = params
    return f.url

def extractJsonFromSeleniumSource():
    global driver

    data = {}

    try:
        pre = driver.find_element_by_tag_name("pre").text
        data = json.loads(pre)
    except:
        print("Exception extracting JSON data, trying again in 10sec")
        logging.warning("CarMax Server Error while scraping, waiting to try again")
        time.sleep(10)
        driver.get(constructUrl())
        extractJsonFromSeleniumSource()

    return data

def addEntriesToList(data):
    global allItemsForSale

    itemSaleList = data["items"]
    for i in range(len(itemSaleList)):
        allItemsForSale.append(itemSaleList[i])

    print(len(allItemsForSale))

#region Selenium Init
driver = webdriver.Chrome()

driver.get(constructUrl())
#endregion

#region Display total CarMax listings
totalListingsToGet = extractJsonFromSeleniumSource()["totalCount"]
print("Listings to scrape: " + str(totalListingsToGet))
#endregion

logging.info("STARTED Scraping " + str(totalListingsToGet) + " listings")

#region Scrape all car listings
allItemsForSale = []

for i in range(math.floor(totalListingsToGet / 1000)):
    driver.get(constructUrl())

    addEntriesToList(extractJsonFromSeleniumSource())

    time.sleep(0.2)

    params["skip"] += 1000

params["take"] = (totalListingsToGet % 1000)

driver.get(constructUrl())
addEntriesToList(extractJsonFromSeleniumSource())
#endregion

csv.exportCSV(exportCSVFilename, allItemsForSale)

print("Exported all listings to " + exportCSVFilename)
logging.info("SUCCESS Scraping " + str(totalListingsToGet) + " listings")








