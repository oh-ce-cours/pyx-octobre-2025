import requests
import datetime


def create_user(base_url, name, email, password):
    payload = {"name": name, "email": email, "password": password}
    resp = requests.post(f"{base_url}/auth/signup", json=payload, timeout=5)

    try:
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la création de l'utilisateur: {e}")
        print(f"Payload: {payload}")
        print(f"Response: {resp.text}")
        if "Duplicate record detected." in resp.text:
            print("Un utilisateur avec cet email existe déjà.")
        return None
    token = resp.json()["authToken"]
    return token


def login_user(base_url, email, password) -> None | str:
    payload = {"email": email, "password": password}
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    resp = requests.post(
        f"{base_url}/auth/login", json=payload, headers=headers, timeout=5
    )
    try:
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la connexion de l'utilisateur: {e}")
        print(f"Payload: {payload}")
        print(f"Response: {resp.text}")
        return None
    token = resp.json()["authToken"]
    return token


def get_logged_user_info(base_url, token):
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    resp = requests.get(f"{base_url}/auth/me", headers=headers, timeout=5)
    try:
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération des informations utilisateur: {e}")
        print(f"Response: {resp.text}")
        return None
    return resp.json()
