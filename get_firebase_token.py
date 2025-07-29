import requests
import json


API_KEY = "AIzaSyB3pFGHqcsSiQJ95DF4rgXSQHiCRNQ6eCo"  
email = "majitomule@gmail.com"    
password = "Prueba123" 

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
