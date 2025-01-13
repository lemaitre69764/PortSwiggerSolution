import sys
import logging
import re
import time

import requests

import utils

log = logging.getLogger(__name__)

class Shop:
    def __init__(self, url, no_proxy, session=None):
        self.base_url = utils.normalize_url(url)
        self.login_url = self.base_url + "login"
        self.no_proxy = no_proxy
        self.session = session
        
        
        
    def get_hint(self):
        log.info("Getting hint")
        if self.no_proxy:
            resp = requests.get(self.base_url)
        else:
            resp = requests.get(self.base_url, proxies=utils.PROXIES, verify=False)
        pattern = re.compile(r'id="hint">.*?: \'(.*?)\'')
        m = pattern.search(resp.text)
        log.info(f"Found hint: {m[1]}")
        return m[1]

        
        
    def login(self, username, password):
        log.info("Geting login page.")
        if self.no_proxy:
            resp = self.session.get(self.login_url)
        else:
            resp = self.session.get(self.login_url, proxies=utils.PROXIES, verify=False)
        if not resp.status_code == 200:
            log.error("Could not get login page. Exiting script.")
            sys.exit()
        pattern = re.compile(r'name="csrf" value="(.*?)"')
        m = pattern.search(resp.text)
        csrf_token = m[1]
        log.info(f"Found CSRF token: {csrf_token}")
        data = {
            "csrf": csrf_token,
            "username": username,
            "password": password,
        }
        log.info("attempting to login")
        if self.no_proxy:
            resp = self.session.post(self.login_url, data=data)
        else:
            resp = self.session.post(
                self.login_url, data=data, proxies=utils.PROXIES, verify=False
            )
        if resp.status_code == 200:
            log.info("Successfully logged in.")
        
        
    def is_solved(self):
        def _is_solved(self):
            log.info("Checking if solved....")
            if self.no_proxy:
                resp = requests.get(self.base_url)
            else:
                resp = requests.get(self.base_url, proxies=utils.PROXIES, verify=False)
            if "Congratulations, you solved the lab!" in resp.text:
                log.info("Lab is solved!")
                return True

        solved = _is_solved(self)
        if solved:
            return True
        else:
            time.sleep(2)
            _is_solved(self)
                
    def get_category(self, category):
        category_filter_url = self.base_url + f"filter?category={category}"
        if self.no_proxy:
            resp = requests.get(category_filter_url)
        else:
            resp = requests.get(category_filter_url, proxies=utils.PROXIES, verify=False
            )
        return resp