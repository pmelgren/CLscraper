## Craigslist Autos Scraper

`clautoscraper` provides utilites to scrape search results from the autos section 
of multiple craigslist sites at once. You may specify entire states, countries,
or even continents across which to search. This package also allows you to specify 
any criteria that craigslist uses to search for autos. 

Please note that this package as written is intended only for personal use and 
should be used in a non-abusive way when interacting with the craigslist site. 
For example, one-time uses across a few states requires far fewer url requests than 
casually browsing the site, but scheduling a high-frequency job to run a scraping 
function found in this package would be taxing on the site and is not acceptable 
per craigslist's user agreement.

#### Example usage:
```
# Query all results for "Jeep" from all craigslist sites in Kansas
import clautoscraper as ca
ca.all_results_from_region('kansas',{'query':'Jeep'})

# Look for all tacomas matching the below criteria in the 6 states below
params = {'query':'tacoma'
	  ,'max_price':7000
	  ,'max_auto_miles':170000
	  ,'auto_cylinders':2
	  ,'auto_drivetrain':3
	  ,'auto_transmission':1
	  }

all_res = []
for r in ['Delaware','kansas','New Jersey','Pennsylvania','ohio','missouri']:
	all_res.append(all_results_from_region(r,params))
```
		


