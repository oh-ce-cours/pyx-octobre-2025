"""
Client API unifié pour l'intégration avec l'API externe.
Utilise les données Faker pour créer des utilisateurs et des VMs via l'API.
"""

import requests
import json
from typing import Dict, Any, List, Optional
from utils.logging_config import get_logger
from utils.config import config
from .exceptions import APIClientError, AuthenticationError, APIRequestError

logger = get_logger(__name__)


class APIClient:
    """Client API unifié pour l'intégration avec l'API externe."""
    
    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initialise le client API.
        
        Args:
            base_url: URL de base de l'API (ex: https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt)
            timeout: Délai d'attente pour les requêtes
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.token: Optional[str] = None
        self.session = requests.Session()
        
        # Configuration des headers par défaut
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        logger.info("Client API initialisé", base_url=self.base_url, timeout=self.timeout)
    
    def authenticate(self, email: str, password: str, signup: bool = False) -> str:
        """
        S'authentifier auprès de l'API.
        
        Args:
            email: Email de l'utilisateur
            password: Mot de passe
            signup: Si True, fait un signup au lieu d'un login
        
        Returns:
            Token d'authentification
            
        Raises:
            AuthenticationError: Si l'authentification échoue
        """
        endpoint = "/auth/signup" if signup else "/auth/login"
        url = f"{self.base_url}{endpoint}"
        
        payload = {
            "email": email,
            "password": password
        }
        
        logger.info("Authentification en cours", endpoint=endpoint, email=email)
        
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            token = data.get("authToken") or data.get("token")
            
            if not token:
                raise AuthenticationError("Token d'authentification non reçu")
            
            self.token = token
            self.session.headers.update({
                'Authorization': f'Bearer {token}'
            })
            
            logger.info("Authentification réussie", token_length=len(token))
            return token
            
        except requests.RequestException as e:
            logger.error("Erreur d'authentification", error=str(e), endpoint=endpoint)
            raise AuthenticationError(f"Échec de l'authentification: {str(e)}")
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Effectue une requête HTTP vers l'API.
        
        Args:
            method: Méthode HTTP (GET, POST, PATCH, DELETE)
            endpoint: Endpoint de l'API (ex: /user, /vm)
            **kwargs: Arguments supplémentaires pour requests
            
        Returns:
            Données de la réponse JSON
            
        Raises:
            APIRequestError: Si la requête échoue
        """
        url = f"{self.base_url}{endpoint}"
        
        # Suppression de timeout si déjà défini
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        
        logger.debug("Requête API", method=method, url=url, authenticated=bool(self.token))
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            
            # Gérer les réponses vides
            if response.status_code == 204:
                return {}
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(
                "Erreur de requête API",
                method=method,
                url=url,
                status_code=getattr(e.response, 'status_code', None),
                error=str(e)
            )
            raise APIRequestError(f"Échec de la requête {method} {endpoint}: {str(e)}")
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée un utilisateur via l'API.
        
        Args:
            user_data: Données de l'utilisateur à créer
            
        Returns:
            Données de l'utilisateur créé
        """
        logger.info("Création d'un utilisateur via l'API", name=user_data.get("name"))
        
        payload = {
            "name": user_data["name"],
            "email": user_data["email"]
            # Ajouter d'autres champs selon l'API
        }
        
        return self._make_request("POST", "/user", json=payload)
    
    def create_vm(self, vm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crée une VM via l'API.
        
        Args:
            vm_data: Données de la VM à créer
            
        Returns:
            Données de la VM créée
        """
        logger.info("Création d'une VM via l'API", name=vm_data.get("name"))
        
        payload = {
            "name": vm_data["name"],
            "operating_system": vm_data["operating_system"],
            "cpu_cores": vm_data["cpu_cores"],
            "ram_gb": vm_data["ram_gb"],
            "disk_gb": vm_data["disk_gb"],
            "status": vm_data.get("status", "running"),
            "user_id": vm_data["user_id"]
        }
        
        return self._make_request("POST", "/vm", json=payload)
    
    def attach_vm_to_user(self, vm_id: int, user_id: int) -> Dict[str, Any]:
        """
        Associe une VM à un utilisateur.
        
        Args:
            vm_id: ID de la VM
            user_id: ID de l'utilisateur
            
        Returns:
            Résultat de l'opération
        """
        logger.info("Association VM-utilisateur", vm_id=vm_id, user_id=user_id)
        
        payload = {
            "vm_id": vm_id,
            "user_id": user_id
        }
        
        return self._make_request("POST", "/Attach_VM_to_user", json=payload)
    
    def stop_vm(self, vm_id: int) -> Dict[str, Any]:
        """
        Arrête une VM.
        
        Args:
            vm_id: ID de la VM
            
        Returns:
            Résultat de l'opération
        """
        logger.info("Arrêt de la VM", vm_id=vm_id)
        
        payload = {
            "vm_id": vm_id
        }
        
        return self._make_request("POST", "/Stop_VM", json=payload)
    
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Récupère tous les utilisateurs.
        
        Returns:
            Liste des utilisateurs
        """
        logger.info("Récupération de所有utilisateurs")
        return self._make_request("GET", "/user")
    
    def get_vms(self) -> List[Dict[str, Any]]:
        """
        Récupère toutes les VMs.
        
        Returns:
            Liste des VMs
        """
        logger.info("Récupération de所有VMs")
        return self._make_request("GET", "/vm")
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Récupère un utilisateur par ID.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Données de l'utilisateur
        """
        return self._make_request("GET", f"/user/{user_id}")
    
    def get_vm(self, vm_id: int) -> Dict[str, Any]:
        """
        Récupère une VM par ID.
        
        Args:
            vm_id: ID de la VM
            
        Returns:
            Données de la VM
        """
        return self._make_request("GET", f"/vm/{vm_id}")
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            user_data: Nouvelles données
            
        Returns:
            Utilisateur mis à jour
        """
        return self._make_request("PATCH", f"/user/{user_id}", json=user_data)
    
    def update_vm(self, vm_id: int, vm_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Met à jour une VM.
        
        Args:
            vm_id: ID de la VM
            vm_data: Nouvelles données
            
        Returns:
            VM mise à jour
        """
        return self._make_request("PATCH", f"/vm/{vm_id}", json=vm_data)
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Supprime un utilisateur.
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Résultat de la suppression
        """
        return self._make_request("DELETE", f"/user/{user_id}")
    
    def delete_vm(self, vm_id: int) -> Dict[str, Any]:
        """
        Supprime une VM.
        
        Args:
            vm_id: ID de la VM
            
        Returns:
            Résultat de la suppression
        """
        return self._make_request("DELETE", f"/vm/{vm_id}")
    
    def get_me(self) -> Dict[str, Any]:
        """
        Récupère les informations de l'utilisateur authentifié.
        
        Returns:
            Données de l'utilisateur authentifié
        """
        return self._make_request("GET", "/auth/me")
