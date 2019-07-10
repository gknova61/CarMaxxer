#!/usr/bin/env python3

"""updateData.py: Adds new sales to database"""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com "

from datetime import datetime
import lib.csvHandler as csv
import lib.ioHandler as io
import lib.sqlliteHandler as sqllite
import logging
import os

logging.basicConfig(filename='carmax-sales-data.log',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

newSalesFilename = "newSales.csv"
masterSalesDatabase = "sales.db"

logging.info("STARTED updateData")

def checkForNewSalesData():
    if not os.path.exists(newSalesFilename):
        print("Error: No sales data found")
        print("Please run compareSalesListings to get a list of used car sales to update")
        logging.info("FAIL updateData")
        logging.error("No sales data found")
        exit(1)

checkForNewSalesData()

newSales = csv.importCSV(newSalesFilename)

#region Push new sales CSV into SQLlite database (sales.db)
sqllite.createConnection(masterSalesDatabase)

newSales[0]['dateAdded'] = datetime.today().strftime('%Y-%m-%d')
sqllite.createTable('sales', newSales[0],['vin','stockNumber'])

duplicateEntries = 0
for row in newSales:
    row['dateAdded'] = datetime.today().strftime('%Y-%m-%d')
    if not sqllite.postRow('sales', row):
        if "UNIQUE constraint failed" in sqllite.getLastException():
            duplicateEntries += 1
        else:
            print("Error: SQLite exception when inserting row")
            print(sqllite.getLastException())
            logging.info("FAIL updateData")
            logging.error(sqllite.getLastException())
            exit(1)

if duplicateEntries > 0:
    logging.warning("Duplicate entries ("+str(duplicateEntries)+") were prevented from being inserted into sales db")

sqllite.commitChanges()
sqllite.closeConnection()
#endregion

io.rename(newSalesFilename,newSalesFilename + ".old")

logging.info("SUCCESS updateData (" + str(len(newSales)-duplicateEntries) + " new sales) ")