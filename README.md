# CarMaxxer
Couldn't find a good used vehicle sales dataset, so here's the scripts I wrote to make one.

## Objective
Collect data on used vehicle sales from CarMax, the United States' largest used-car retailer. 

## Python 3.7 Package Dependencies
  - furl (URL Manipulation)
  - Selenium (
  - ChromeDriver for Selenium
  
## Instructions
Ideally, these are ran on a cron-job:
  1. Run listingScraper.py
  2. Run compareSalesListings.py
  3. Run updateData.py
  4. Wait and repeat

Scripts will need to be run through at least once (with some time apart for new sales) before a sales.db SQLite database shows in the working directory.
