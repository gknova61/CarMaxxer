#!/usr/bin/env python3

"""dbHealthCheck.py: Script for checking database integrity"""

__author__      = "Keanu Kauhi-Correia"
__version__ = "1.0"
__maintainer__ = "Keanu Kauhi-Correia"
__email__ = "keanu.kkc@gmail.com"

import lib.sqlliteHandler as sqllite
import logging
import os

logging.basicConfig(filename='carmax-sales-data.log',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.DEBUG)

def hasDuplicates(data,index):
    buffer = []
    for row in data:
        if row[index] not in buffer:
            buffer.append(row[index])
        else:
            return True

    return False


logging.info("STARTED dbHealthCheck")

if not os.path.exists('sales.db'):
    print("ERROR: Database not found")
    logging.info("FAIL dbHealthCheck")
    logging.error("SQLite Database file not found")
    exit(1)

sqllite.createConnection('sales.db')

database = sqllite.executeRawQuery('SELECT * FROM sales').fetchall()

healthChecksFailed = []

if hasDuplicates(database,0):
    print("Database has duplicate stock numbers")
    healthChecksFailed.append("dupeVIN")

if hasDuplicates(database,1):
    print("Database has duplicate VINs")
    healthChecksFailed.append("dupeStockNumber")

sqllite.closeConnection()

logging.info("SUCCESS dbHealthCheck")
if len(healthChecksFailed) < 1:
    logging.info("PASS ALL HEALTH CHECKS")
else:
    logging.info("FAILED HEALTH CHECK ("+', '.join(healthChecksFailed)+")")