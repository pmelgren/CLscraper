# Script to scrape historical NCAA Men's basketball odds data from
# sportsbook reviews online's odds archive.

import requests
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd

def get_text(obj):
    return None if obj is None else obj.text


def url_to_bs(url):
    
    #parse the htm from the craigslist site page
    with closing(requests.get(url)) as page:
        raw = page.content
    return BeautifulSoup(raw, 'html.parser')


def get_all_cl_sites(region = 'US'):
    """Get Excel Links
    
    Get a named dictionary of all craigslist sites located on a given continent
    
    Arguments:
        region (str): The region (continent, state or country) to get all sites
            from on the craigslist site page. Case should not matter.
    
    Return (dict): A dict with every link under that region named according to
        the site name.
        
    """
    
    #get a beautifulsoup object from the craigslist sites page
    soup = url_to_bs('https://www.craigslist.org/about/sites')
    
    # check every continent or state/country to see if any match the region
    # argument and if so return the corresponding section
    for h in soup.body.section.find_all('h1')+soup.body.section.find_all('h4'):
        
        #if it matches get the BS object for the following section
        if h.text.upper() == region.upper():
            cont = h.next_sibling.next_sibling 
            break
        
    #raise an exception if it can't find the region
    else: 
        raise Exception('Could not find region: '+region)
    
    
    #put all the links into a dictionary
    all_sites = {}
    for c in cont.find_all('a'):
        all_sites.update({c.text : c['href']})
    
    return all_sites

sites = get_all_cl_sites('new jersey')

params = {'query':'toyota tacoma'
          ,'max_price':10000
          ,'max_auto_miles':355000
          ,'auto_cylinders':2
          ,'auto_drivetrain':3
          ,'auto_transmission':1
          }

all_results = []
for s,l in sites.items():
    search_url = l+'search/cta?'+'&'.join("{!s}={!r}".format(key,val) 
                                            for (key,val) in params.items())
    soup = url_to_bs(search_url)
    
    #parse through all search results 
    for c in soup.find('ul',{'class','rows'}).children:
        if c == '\n':
            continue
        
        #stop once we reach non-local search results
        if c.name == 'h4':
            break
        
        #store the link and pricing information
        all_results.append({
                'site':s
                ,'location':get_text(c.find('span',{'class','result-hood'}))
                ,'title':get_text(c.find('a',{'class','result-title hdrlnk'}))
                ,'price':get_text(c.find('span',{'class','result-price'}))
                ,'link':c.find('a',{'class','result-title hdrlnk'})['href']
                })
            
pd.set_option('display.max_column',None)
print(pd.DataFrame(all_results)) 