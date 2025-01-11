import utils

class Shop():
    def __init__(self, url):
        self.base_url = utils.normalize_url(url)
        self.login_url = self.base_url + "login"  
        
        

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
                