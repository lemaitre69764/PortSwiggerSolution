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
    """
    Почему важен return?
    Без return функция ничего не вернёт, и вы не сможете получить доступ
    к обработанным аргументам.
    """

def normalize_url(url):
    if not url.endswith("/"):
        url = url + "/"
    return url


def is_solved(url, no_proxy):
    def _is_solved(url, no_proxy): # underline like a private to class 
        log.info("Checking if solved.")
        if no_proxy:
            resp = requests.get(url)
        else:
            resp = requests.get(url, proxies=PROXIES, verify=False)
        if "Congratulations, you solved the lab!" in resp.text:
            log.info("Lab is solved!")
            return True
        
    solved = _is_solved(url, no_proxy)
    if solved:
        return True
    else:
        time.sleep(2)
        _is_solved(url, no_proxy)
        