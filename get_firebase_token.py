import requests
import json

# Reemplaza estos valores por los de tu proyecto y usuario
API_KEY = "AIzaSyB3pFGHqcsSiQJ95DF4rgXSQHiCRNQ6eCo"  # <-- Pon aquí tu API_KEY de Firebase
email = "majitomule@gmail.com"       # <-- Pon aquí el email del usuario
password = "Prueba123" # <-- Pon aquí la contraseña del usuario

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

if response.status_code == 200:
    id_token = response.json()["idToken"]
    print("ID Token:", id_token)
else:
    print("Error:", response.json()) 