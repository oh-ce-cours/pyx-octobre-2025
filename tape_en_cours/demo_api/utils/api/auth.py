import requests
from utils.logging_config import get_logger
from .exceptions import UserCreationError, UserLoginError, UserInfoError, TokenError

# Logger pour ce module
logger = get_logger(__name__)


class Auth:
    """
    Classe d'authentification pour l'API demo_api.

    Gère la création d'utilisateurs, la connexion et la récupération
    des informations utilisateur via les endpoints d'authentification.
    """

    def __init__(self, base_url):
        """
        Initialise le client d'authentification.

        Args:
            base_url (str): URL de base de l'API
        """
        self.base_url = base_url

    def create_user(self, name, email, password):
        """
        Crée un nouvel utilisateur via l'endpoint /auth/signup.

        Args:
            name (str): Nom de l'utilisateur
            email (str): Email de l'utilisateur
            password (str): Mot de passe de l'utilisateur

        Returns:
            str: Token d'authentification généré

        Raises:
            UserCreationError: Si la création de l'utilisateur échoue
        """
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
                f"{self.base_url}/auth/signup", json=payload, timeout=5
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
                ) from e

            # Autres erreurs de création
            raise UserCreationError(
                f"Impossible de créer l'utilisateur {email}: {str(e)}",
                status_code=getattr(resp, "status_code", None),
                response_data={"error": str(e), "email": email},
                email=email,
            ) from e

    def login_user(self, email, password) -> str:
        """
        Connecte un utilisateur existant via l'endpoint /auth/login.

        Args:
            email (str): Email de l'utilisateur
            password (str): Mot de passe de l'utilisateur

        Returns:
            str: Token d'authentification généré

        Raises:
            UserLoginError: Si la connexion échoue
        """
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
                f"{self.base_url}/auth/login", json=payload, headers=headers, timeout=5
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
            ) from e

    def get_logged_user_info(self, token):
        """
        Récupère les informations de l'utilisateur connecté via l'endpoint /auth/me.

        Args:
            token (str): Token d'authentification

        Returns:
            dict: Informations de l'utilisateur connecté

        Raises:
            TokenError: Si le token est manquant
            UserInfoError: Si la récupération des informations échoue
        """
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
            resp = requests.get(f"{self.base_url}/auth/me", headers=headers, timeout=5)
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
            ) from e
