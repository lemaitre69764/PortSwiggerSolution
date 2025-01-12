import sys
import argparse


PROXIES = {
    "http": "127.0.0.1:8080",
    "https": "127.0.0.1:8080",
}


def parse_args(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--no-proxy", default=False, action="store_true", help="do not use proxy"
    )
    parser.add_argument("url", help="url of lab")
    return parser.parse_args() 


def parse_args_collab(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--no-proxy", default=False, action="store_true", help="do not use proxy"
    )
    parser.add_argument("url", help="url of lab")
    parser.add_argument("collab", help="collaborator domain")
    return parser.parse_args() 


def normalize_url(url):
    if not url.endswith("/"):
        url = url + "/"
    return url

