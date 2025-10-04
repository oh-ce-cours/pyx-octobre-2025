import requests
import datetime
from ..logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)


class Auth:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, name, email, password):
        logger.info("Tentative de création d'utilisateur", email=email, name=name)
        payload = {"name": name, "email": email, "password": password}
        logger.debug(
            "Payload de création (password masqué)",
            name=name,
            email=email,
            password="[HIDDEN]",
            base_url=self.base_url,
        )
        resp = requests.post(f"{self.base_url}/auth/signup", json=payload, timeout=5)

        try:
            resp.raise_for_status()
            logger.info(
                "Utilisateur créé avec succès",
                email=email,
                status_code=resp.status_code,
            )
        except requests.RequestException as e:
            logger.error(
                "Erreur lors de la création de l'utilisateur",
                error=str(e),
                status_code=resp.status_code,
                response_text=resp.text[:200] + "..."
                if len(resp.text) > 200
                else resp.text,
                email=email,
            )
            if "Duplicate record detected." in resp.text:
                logger.warning("Utilisateur déjà existant", email=email)
            return None
        token = resp.json()["authToken"]
        logger.debug(
            "Token généré pour nouveau utilisateur",
            email=email,
            token_length=len(token),
        )
        return token

    def login_user(self, email, password) -> None | str:
        logger.info("Tentative de connexion utilisateur", email=email)
        payload = {"email": email, "password": password}
        logger.debug("Payload de connexion (password masqué)", 
                    email=email, 
                    password="[HIDDEN]",
                    base_url=self.base_url)
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        resp = requests.post(
            f"{self.base_url}/auth/login", json=payload, headers=headers, timeout=5
        try:
            resp.raise_for_status()
            logger.info("Utilisateur connecté avec succès", email=email, status_code=resp.status_code)
        except requests.RequestException as e:
            logger.error("Erreur lors de la connexion utilisateur", 
                        error=str(e), 
                        status_code=resp.status_code,
                        response_text=resp.text[:200] + "..." if len(resp.text) > 200 else resp.text,
                        email=email)
            return None
        token = resp.json()["authToken"]
        logger.debug("Token généré pour connexion", email=email, token_length=len(token))
        return token

    def get_logged_user_info(self, token):
        headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
        resp = requests.get(f"{self.base_url}/auth/me", headers=headers, timeout=5)
        try:
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des informations utilisateur: {e}")
            print(f"Response: {resp.text}")
            return None
        return resp.json()
