import requests
from utils.logging_config import get_logger
from utils.config import Config
from .exceptions import UserCreationError, UserLoginError, UserInfoError, TokenError

# Logger pour ce module
logger = get_logger(__name__)

# Configuration centralisée
config = Config()


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

        try:
            resp = requests.post(
                f"{self.base_url}/auth/signup",
                json=payload,
                timeout=config.DEMO_API_TIMEOUT,
            )
            resp.raise_for_status()

            logger.info(
                "Utilisateur créé avec succès",
                email=email,
                status_code=resp.status_code,
            )

            token = resp.json()["authToken"]
            logger.debug(
                "Token généré pour nouveau utilisateur",
                email=email,
                token_length=len(token),
            )
            return token

        except requests.RequestException as e:
            logger.error(
                "Erreur lors de la création de l'utilisateur",
                error=str(e),
                status_code=getattr(resp, "status_code", None),
                response_text=getattr(resp, "text", "")[:200] + "..."
                if len(getattr(resp, "text", "")) > 200
                else getattr(resp, "text", ""),
                email=email,
            )

            # Vérifier si c'est un utilisateur déjà existant
            if "Duplicate record detected." in getattr(resp, "text", ""):
                logger.warning("Utilisateur déjà existant", email=email)
                raise UserCreationError(
                    f"Utilisateur déjà existant avec l'email {email}",
                    status_code=getattr(resp, "status_code", None),
                    response_data={"error": "duplicate_user", "email": email},
                    email=email,
                )

            # Autres erreurs de création
            raise UserCreationError(
                f"Impossible de créer l'utilisateur {email}: {str(e)}",
                status_code=getattr(resp, "status_code", None),
                response_data={"error": str(e), "email": email},
                email=email,
            )

    def login_user(self, email, password) -> str:
        logger.info("Tentative de connexion utilisateur", email=email)
        payload = {"email": email, "password": password}
        logger.debug(
            "Payload de connexion (password masqué)",
            email=email,
            password="[HIDDEN]",
            base_url=self.base_url,
        )
        headers = {"accept": "application/json", "Content-Type": "application/json"}

        try:
            resp = requests.post(
                f"{self.base_url}/auth/login",
                json=payload,
                headers=headers,
                timeout=config.DEMO_API_TIMEOUT,
            )
            resp.raise_for_status()

            logger.info(
                "Utilisateur connecté avec succès",
                email=email,
                status_code=resp.status_code,
            )

            token = resp.json()["authToken"]
            logger.debug(
                "Token généré pour connexion", email=email, token_length=len(token)
            )
            return token

        except requests.RequestException as e:
            logger.error(
                "Erreur lors de la connexion utilisateur",
                error=str(e),
                status_code=getattr(resp, "status_code", None),
                response_text=getattr(resp, "text", "")[:200] + "..."
                if len(getattr(resp, "text", "")) > 200
                else getattr(resp, "text", ""),
                email=email,
            )

            raise UserLoginError(
                f"Impossible de se connecter avec l'email {email}: {str(e)}",
                status_code=getattr(resp, "status_code", None),
                response_data={"error": str(e), "email": email},
                email=email,
            )

    def get_logged_user_info(self, token):
        if not token:
            logger.error("Token manquant pour récupérer les informations utilisateur")
            raise TokenError(
                "Token manquant pour récupérer les informations utilisateur",
                token_length=0,
            )

        logger.info(
            "Récupération des informations utilisateur", token_length=len(token)
        )
        headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}

        try:
            resp = requests.get(
                f"{self.base_url}/auth/me",
                headers=headers,
                timeout=config.DEMO_API_TIMEOUT,
            )
            resp.raise_for_status()

            user_info = resp.json()
            logger.info(
                "Informations utilisateur récupérées",
                user_id=user_info.get("id"),
                user_name=user_info.get("name"),
                email=user_info.get("email"),
            )
            return user_info

        except requests.RequestException as e:
            logger.error(
                "Erreur lors de la récupération des informations utilisateur",
                error=str(e),
                status_code=getattr(resp, "status_code", None),
                response_text=getattr(resp, "text", "")[:200] + "..."
                if len(getattr(resp, "text", "")) > 200
                else getattr(resp, "text", ""),
                token_length=len(token),
            )

            raise UserInfoError(
                f"Impossible de récupérer les informations utilisateur: {str(e)}",
                status_code=getattr(resp, "status_code", None),
                response_data={"error": str(e)},
                token_length=len(token),
            )
