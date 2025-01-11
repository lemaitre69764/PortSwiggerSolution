import sys
import logging


import utils

log = logging.getLogger(__name__)

class Shop:
    def __init__(self, url, no_proxy, session):
        self.base_url = utils.normalize_url(url)
        self.login_url = self.base_url + "login"
        self.no_proxy = no_proxy
        self.session = session
        
    def login(self, username, password):
        log.info("Geting login page.")
        if self.no_proxy:
            resp = self.session.get(self.login_url)
        else:
            resp = self.session.get(self.login_url, proxies=utils.PROXIES, verify=False)
        if not resp.status_code == 200:
            log.error("Could not get login page. Exiting script.")
            sys.exit()
        

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
                