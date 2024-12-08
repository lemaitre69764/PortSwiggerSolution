import requests

def check_solution_direct(url):
    log.info("Checking if solved directly.")
    resp = requests.get(url) 
    return analyze_response(resp)

def check_solution_with_proxy(url):
    log.info("Checking if solved through proxy.")
    resp = requests.get(url, proxies=PROXIES, verify=False) 
    return analyze_response(resp)

def analyze_response(resp):
    if "Congratulations, you solved the lab!" in resp.text:
        log.info("Lab is solved!")
        return True
    return False
 
def retrieve_contents(url, no_proxy):
    if no_proxy:
        return check_solution_direct(url)   
    else:
        return check_solution_with_proxy(url)   

def is_solved(url, no_proxy):
    log.info("Checking if lab is solved...")
    solved = retrieve_contents(url, no_proxy)  
    if solved:
        return True  
    else:
        log.info("Lab not solved yet, retrying...")  
        time.sleep(2)  
        return retrieve_contents(url, no_proxy) 
------------------------------------------------------------------------------------------
def is_solved(url, no_proxy):
    def retrieve_contents(url, no_proxy): #вложенная функция (nested function) функция, определённая внутри другой функции ;)
        log.info("Checking if solved.") #сделали код компактным проще говоря
        if no_proxy:
            resp = requests.get(url)
        else:
            resp = requests.get(url, proxies=PROXIES, verify=False)
        if "Congratulations, you solved the lab!" in resp.text:
            log.info("Lab is solved!")
            return True
        
    solved = retrieve_contents(url, no_proxy)
    if solved:
        return True
    else:
        time.sleep(2)
        retrieve_contents(url, no_proxy)
