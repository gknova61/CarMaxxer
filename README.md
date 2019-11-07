# CarMaxxer
Couldn't find a good used vehicle sales dataset, so here is what I wrote to make one based on CarMax's listings.

## Objective
Collect data on used vehicle sales from [CarMax](https://www.carmax.com/cars), the United States' largest used-car retailer. 

## Python 3.7 Package Dependencies
  - furl (URL Manipulation)
  - Selenium
  - ChromeDriver for Selenium
  
## Instructions
Ideally, these are ran on a cron-job:
  1. Run listingScraper.py
  2. Run compareSalesListings.py
  3. Run updateData.py
  4. Wait and repeat

After the first two runs (with some time apart for new sales), a `sales.db` file will be generated. This is an SQLite database that will show in the current working directory.
