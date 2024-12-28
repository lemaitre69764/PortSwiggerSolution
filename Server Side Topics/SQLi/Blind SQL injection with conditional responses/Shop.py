import utils

class Shop():
    def __init__(self, url, sess, no_proxy):
        self.base_url = utils.normalize_url(url)
        self.login_url = self.base_url + "login" 
        #self.no_proxy = no_proxy
        #self.sess = sess