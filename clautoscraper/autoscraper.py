import requests
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd


def get_text(obj):
    """Small helper function to get the text from a Beautiful Soup object 
    unless it is None in which case return None"""
    
    return None if obj is None else obj.text

#
def url_to_bs(url):
    """FUnction to take a url and return a BeautifulSoup object of that page's
    parsed content"""    

    with closing(requests.get(url)) as page:
        raw = page.content
    return BeautifulSoup(raw, 'html.parser')


def get_all_cl_sites(region):
    """Get All Craigslist Sites
    
    Get a named dictionary of all craigslist sites from a given region.
    
    Arguments:
        region (str): The region (continent, state or country) to get all sites
            from on the craigslist site page. All valid regions can be found at
            https://www.craigslist.org/about/sites
    
    Return (dict): A dict with every link under that region named according to
        the site name.
        
    Examples:
        >>> get_all_cl_sites('nevada')
        {'elko': 'https://elko.craigslist.org/',
         'las vegas': 'https://lasvegas.craigslist.org/',
         'reno / tahoe': 'https://reno.craigslist.org/'}
        
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

def all_results_from_region(region, params):
    """All Results from Region
    
    For a given craigslist region (i.e. US, Pennsylvania), return  certain 
    metadata from all results of a search of the cars + trucks section as
    specified by the search parameters stored in params.
    
    Arguments:
        region (str): The region (continent, state or country) to get all sites
            from on the craigslist site page. Case should not matter.
        params (dict): The search parameters to feed to Craigslist
    
    Return (list): A list of dict's that will contain metadata
    
    Example:
        >>> params = {'query':'tacoma'
                      ,'max_price':7000
                      ,'max_auto_miles':170000
                      ,'auto_cylinders':2
                      ,'auto_drivetrain':3
                      ,'auto_transmission':1
                      }

        >>> all_results_from_region('kansas',params)
        [{'site': 'wichita',
          'location': ' (Wichita KS)',
          'title': '2002 Toyota Tacoma 4x4 Extended Cab OBO',
          'price': '$6599',
          'link': 'https://wichita.craigslist.org/cto/d/.../.html'}]
        
        
    """
    
    all_results = []

    #return each of the sites found in a given region
    sites = get_all_cl_sites(region)
    
    #loop through each site and get the search result parameters
    for s,l in sites.items():
        
        #compose the search url then parse the resulting html
        search_url = l+'search/cta?'+'&'.join("{!s}={!r}".format(key,val) 
                                              for (key,val) in params.items())
        soup = url_to_bs(search_url)
        
        #parse through all search results 
        for c in soup.find('ul',{'class','rows'}).children:
            if c == '\n':
                continue
            
            #stop if we reach non-local search results
            if c.name == 'h4':
                break
            
            #store the link and pricing information in a dict
            all_results.append({
                    'site':s
                    ,'location':get_text(c.find('span',{'class','result-hood'}))
                    ,'title':get_text(c.find('a',{'class','result-title hdrlnk'}))
                    ,'price':get_text(c.find('span',{'class','result-price'}))
                    ,'link':c.find('a',{'class','result-title hdrlnk'})['href']
                    })
                
    return all_results