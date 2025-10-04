"""
API unifiée pour demo_api

Interface fluide pour accéder aux fonctionnalités de l'API :
- Api(base_url).users.get()
- Api(base_url).vms.get()
- Api(base_url).login(email, password)
- Api(base_url).users.create_vm(...)
"""

from typing import Optional, Dict, Any, List
from .auth import Auth
from .user import (
    get_users,
    add_vms_to_users,
    create_user,
    get_user,
    update_user,
    delete_user,
)
from .vm import (
    get_vms,
    create_vm,
    get_vm,
    update_vm,
    delete_vm,
    attach_vm_to_user,
    stop_vm,
)
from .exceptions import (
    UserCreationError,
    UserLoginError,
    TokenError,
)
from ..config import config
from ..logging_config import get_logger

logger = get_logger(__name__)


class UsersAPI:
    """Interface pour les opérations sur les utilisateurs"""

    def __init__(self, api_client: "ApiClient"):
        self._api = api_client

    def get(self) -> List[Dict[str, Any]]:
        """Récupère la liste des utilisateurs"""
        logger.info("Récupération des utilisateurs via API unifiée")
        return get_users(self._api.base_url)

    def add_vms_to_users(self, users: List[Dict], vms: List[Dict]) -> None:
        """Associe les VMs aux utilisateurs"""
        logger.info("Association des VMs aux utilisateurs via API unifiée")
        add_vms_to_users(users, vms)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Récupère un utilisateur spécifique par son ID
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Dict contenant les informations de l'utilisateur
            
        Raises:
            UsersFetchError: Si la récupération de l'utilisateur échoue
        """
        logger.info("Récupération d'un utilisateur spécifique via API unifiée", user_id=user_id)
        return get_user(self._api.base_url, user_id)

    def create_user(self, name: str, email: str, password: Optional[str] = None) -> Dict[str, Any]:
        """Crée un nouvel utilisateur
        
        Args:
            name: Nom de l'utilisateur
            email: Email de l'utilisateur
            password: Mot de passe optionnel
            
        Returns:
            Dict contenant les informations de l'utilisateur créé
            
        Raises:
            UserCreationError: Si la création de l'utilisateur échoue
        """
        logger.info("Création d'un utilisateur via API unifiée", name=name, email=email)
        return create_user(self._api.base_url, self._api.token, name, email, password)

    def update_user(self, user_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Met à jour un utilisateur existant
        
        Args:
            user_id: ID de l'utilisateur
            updates: Données à mettre à jour
            
        Returns:
            Dict contenant les informations de l'utilisateur mis à jour
            
        Raises:
            UserUpdateError: Si la mise à jour échoue
        """
        logger.info("Mise à jour d'un utilisateur via API unifiée", user_id=user_id)
        return update_user(self._api.base_url, self._api.token, user_id, updates)

    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Supprime un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Dict contenant le résultat de la suppression
            
        Raises:
            UserDeleteError: Si la suppression échoue
        """
        logger.info("Suppression d'un utilisateur via API unifiée", user_id=user_id)
        return delete_user(self._api.base_url, self._api.token, user_id)

    def create_vm(
        self,
        user_id: int,
        name: str,
        operating_system: str,
        cpu_cores: int,
        ram_gb: int,
        disk_gb: int,
        status: str = "stopped",
    ) -> Dict[str, Any]:
        """Crée une VM pour un utilisateur

        Raises:
            VMCreationError: Si la création de la VM échoue
        """
        logger.info(
            "Création de VM via API unifiée",
            user_id=user_id,
            name=name,
            operating_system=operating_system,
        )
        return create_vm(
            self._api.token,
            self._api.base_url,
            user_id=user_id,
            name=name,
            operating_system=operating_system,
            cpu_cores=cpu_cores,
            ram_gb=ram_gb,
            disk_gb=disk_gb,
            status=status,
        )


class VMsAPI:
    """Interface pour les opérations sur les VMs"""

    def __init__(self, api_client: "ApiClient"):
        self._api = api_client

    def get(self) -> List[Dict[str, Any]]:
        """Récupère la liste des VMs"""
        logger.info("Récupération des VMs via API unifiée")
        return get_vms(self._api.base_url)

    def create(
        self,
        user_id: int,
        name: str,
        operating_system: str,
        cpu_cores: int,
        ram_gb: int,
        disk_gb: int,
        status: str = "stopped",
    ) -> Dict[str, Any]:
        """Crée une VM

        Raises:
            VMCreationError: Si la création de la VM échoue
        """
        logger.info(
            "Création de VM via API unifiée",
            user_id=user_id,
            name=name,
            operating_system=operating_system,
        )
        return create_vm(
            self._api.token,
            self._api.base_url,
            user_id=user_id,
            name=name,
            operating_system=operating_system,
            cpu_cores=cpu_cores,
            ram_gb=ram_gb,
            disk_gb=disk_gb,
            status=status,
        )


class AuthAPI:
    """Interface pour les opérations d'authentification"""

    def __init__(self, api_client: "ApiClient"):
        self._api = api_client

    def login(self, email: str, password: str) -> str:
        """Connexion d'un utilisateur

        Raises:
            UserLoginError: Si la connexion échoue
        """
        logger.info("Connexion utilisateur via API unifiée", email=email)
        token = self._api._auth.login_user(email, password)
        self._api.token = token
        logger.info("Connexion réussie via API unifiée", email=email)
        return token

    def create_user(self, name: str, email: str, password: str) -> str:
        """Création d'un utilisateur

        Raises:
            UserCreationError: Si la création d'utilisateur échoue
        """
        logger.info("Création utilisateur via API unifiée", email=email, name=name)
        token = self._api._auth.create_user(name, email, password)
        self._api.token = token
        logger.info("Utilisateur créé avec succès via API unifiée", email=email)
        return token

    def get_user_info(self) -> Dict[str, Any]:
        """Récupère les informations de l'utilisateur connecté

        Raises:
            TokenError: Si aucun token n'est disponible
            UserInfoError: Si la récupération des informations échoue
        """
        if not self._api.token:
            logger.warning(
                "Aucun token disponible pour récupérer les informations utilisateur"
            )
            raise TokenError(
                "Aucun token disponible pour récupérer les informations utilisateur"
            )

        logger.info("Récupération des informations utilisateur via API unifiée")
        return self._api._auth.get_logged_user_info(self._api.token)


class ApiClient:
    """Client API unifié avec interface fluide"""

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        """
        Initialise le client API

        Args:
            base_url: URL de base de l'API (utilise config par défaut)
            token: Token d'authentification (optionnel)
        """
        self.base_url = base_url or config.DEMO_API_BASE_URL
        self.token = token or config.DEMO_API_TOKEN
        self._auth = Auth(self.base_url)

        # Interfaces spécialisées
        self.users = UsersAPI(self)
        self.vms = VMsAPI(self)
        self.auth = AuthAPI(self)

        logger.info(
            "Client API unifié initialisé",
            base_url=self.base_url,
            has_token=bool(self.token),
        )

    def login(self, email: str, password: str) -> str:
        """Méthode de connexion directe (raccourci)"""
        return self.auth.login(email, password)

    def create_user(self, name: str, email: str, password: str) -> str:
        """Méthode de création d'utilisateur directe (raccourci)"""
        return self.auth.create_user(name, email, password)

    def get_user_info(self) -> Dict[str, Any]:
        """Méthode d'information utilisateur directe (raccourci)"""
        return self.auth.get_user_info()

    def is_authenticated(self) -> bool:
        """Vérifie si le client est authentifié"""
        return bool(self.token)

    def set_token(self, token: str) -> None:
        """Définit le token d'authentification"""
        self.token = token
        logger.info("Token défini pour le client API", token_length=len(token))

    def clear_token(self) -> None:
        """Supprime le token d'authentification"""
        self.token = None
        logger.info("Token supprimé du client API")

    def __repr__(self) -> str:
        """Représentation du client API"""
        return f"ApiClient(base_url='{self.base_url}', authenticated={self.is_authenticated()})"


# Alias pour une utilisation plus simple
Api = ApiClient


# Fonction utilitaire pour créer un client avec authentification automatique
def create_authenticated_client(
    base_url: Optional[str] = None,
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> ApiClient:
    """
    Crée un client API avec authentification automatique

    Args:
        base_url: URL de base de l'API
        email: Email pour l'authentification
        password: Mot de passe pour l'authentification

    Returns:
        ApiClient: Client API authentifié
    """
    client = ApiClient(base_url)

    # Essayer d'abord avec les identifiants fournis
    if email and password:
        try:
            client.login(email, password)
            return client
        except UserLoginError:
            logger.warning(
                "Échec de connexion avec les identifiants fournis", email=email
            )

    # Essayer avec les identifiants de la configuration
    if config.has_credentials:
        try:
            client.login(config.DEMO_API_EMAIL, config.DEMO_API_PASSWORD)
            return client
        except UserLoginError:
            logger.warning("Échec de connexion avec les identifiants de configuration")

    # Si pas d'authentification, retourner le client sans token
    logger.warning("Aucune authentification réussie, client créé sans token")
    return client
