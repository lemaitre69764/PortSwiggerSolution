import requests
from requests.utils import quote

def load_list_from_file(file_path):
  
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] файл '{file_path}' не найден.")
        return []

def send_payload(url, payload, search_param="search"):
  
    encoded_payload = quote(payload)
    full_url = f"{url}?{search_param}={encoded_payload}"
    
    try:
        response = requests.get(full_url)
        print(f"[*] Тестируем пейлоад: {payload}")
        print(f"Статус-код: {response.status_code}")
        if response.status_code == 200:
            print(f"Ответ сервера: {response.text[:6700]}")
        else:
            print("[-] укщк.")
        print("-" * 40)
        return response.status_code, response.text
    except requests.RequestException as error:
        print(f"[!]eror: {error}")
        return None, None
#stop
