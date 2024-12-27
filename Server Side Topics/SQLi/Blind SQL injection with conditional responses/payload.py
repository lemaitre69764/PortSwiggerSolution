import sys
import logging
import urllib3
import concurrent.futures

import requests

import utils
from shop import Shop

"""ne zabyt here"""
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}][{levelname}] [{name}] {message}",
    style = "{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def determine_response_length(inner_query, url, no_proxy=False):
    log.info("Determining response length for query.")
    sess = requests.Session()
    for i in range(1, 5):
        outer_query = format_length_query(inner_query, i)
        