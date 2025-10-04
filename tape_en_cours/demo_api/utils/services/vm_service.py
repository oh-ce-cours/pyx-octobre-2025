"""
Service de gestion des VMs
"""

from typing import Dict, Any, Optional
from utils.api import Api
from utils.api.exceptions import VMCreationError, UsersFetchError, UserInfoError, TokenError
from utils.logging_config import get_logger
from utils.password_utils import get_or_create_token

logger = get_logger(__name__)


class VMService:
    """Service pour la gestion des VMs"""
    
    def __init__(self, api_client: Api):
        """
        Initialise le service VM
        
        Args:
            api_client: Client API unifié
        """
        self.api = api_client
    
    def authenticate_user(self, email: str = "jean@dupont21.com", password: str = None) -> Optional[Dict[str, Any]]]:
        """
        Authentifie un utilisateur et retourne ses informations
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe de l'utilisateur
            
        Returns:
            Informations de l'utilisateur ou None si l'authentification échoue
        """
        logger.info("Début du processus d'authentification pour création de VM")
        
        try:
            token = get_or_create_token(
                base_url=self.api.base_url,
                email=email,
                password=password,
                token_env_var="DEMO_API_TOKEN",
            )
            
            # Définir le token dans le client API
            self.api.set_token(token)
            logger.info("Token défini dans le client API pour création de VM")
            
            # Récupérer les informations utilisateur
            if self.api.is_authenticated():
                logger.info("Récupération des informations utilisateur authentifié")
                try:
                    user = self.api.get_user_info()
                    logger.info(
                        "Informations utilisateur récupérées pour création VM",
                        user_id=user.get("id"),
                        user_name=user.get("name"),
                    )
                    return user
                except UserInfoError as e:
                    logger.error("Impossible de récupérer les informations utilisateur", error=str(e))
                    return None
            else:
                logger.error("Aucun token disponible après authentification")
                return None
                
        except Exception as e:
            logger.error("Erreur d'authentification", error=str(e))
            return None
    
    def create_vm_for_user(
        self, 
        user: Dict[str, Any], 
        vm_config: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Crée une VM pour un utilisateur spécifique
        
        Args:
            user: Informations de l'utilisateur
            vm_config: Configuration de la VM à créer
            
        Returns:
            Résultat de la création ou None si échec
        """
        if not self.api.is_authenticated():
            logger.error("API non authentifiée pour la création de VM")
            return None
            
        logger.info("Début de création de VM", **vm_config)
        
        try:
            vm_result = self.api.users.create_vm(**vm_config)
            logger.info(
                "VM créée avec succès", 
                vm_id=vm_result.get("id"), 
                status=vm_config.get("status")
            )
            return vm_result
        except VMCreationError as e:
            logger.error("Échec de la création de VM", error=str(e), user_id=user["id"])
            return None
    
    def create_default_vm_for_user(self, user: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crée une VM par défaut pour un utilisateur
        
        Args:
            user: Informations de l'utilisateur
            
        Returns:
            Résultat de la création ou None si échec
        """
        vm_config = {
            "user_id": user["id"],
            "name": "VM de Jean",
            "operating_system": "Ubuntu 22.04",
            "cpu_cores": 2,
            "ram_gb": 4,
            "disk_gb": 50,
            "status": "stopped",
        }
        
        return self.create_vm_for_user(user, vm_config)
