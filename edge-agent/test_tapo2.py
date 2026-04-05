import requests
import hashlib

ip = "10.109.68.15"
username = "Mateoramirez"
password = "mateo1234"

hashed_pass = hashlib.md5(password.encode()).hexdigest().upper()
hashed_user = hashlib.md5(username.encode()).hexdigest()

url = f"http://{ip}/cgi-bin/api.cgi"
payload = {
    "method": "login",
    "params": {
        "username": username,
        "passwd": hashed_pass
    }
}

r = requests.post(url, json=payload, timeout=5)
print("Status:", r.status_code)
print("Response:", r.text)
