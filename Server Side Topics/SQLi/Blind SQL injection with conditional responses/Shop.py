import utils

class Shop():
    def __init__(self, url):
        self.base_url = utils.normalize_url(url)
        self.login_url = self.base_url + "login"  