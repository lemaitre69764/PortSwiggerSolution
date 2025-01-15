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

def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    num_columns = utils.determine_number_of_columns(shop.category_url, shop.no_proxy)
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)
