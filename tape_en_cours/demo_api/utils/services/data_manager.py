"""
Gestionnaire de données centralisé pour éviter les requêtes multiples
"""

from typing import Dict, Any, List, Optional, Tuple
from utils.api import Api
from utils.api.exceptions import UsersFetchError, VMsFetchError
from utils.logging_config import get_logger

logger = get_logger(__name__)


class DataManager:
    """Gestionnaire centralisé des données pour éviter les requêtes multiples"""

    def __init__(self, api_client: Api):
        """
        Initialise le gestionnaire de données

        Args:
            api_client: Client API unifié
        """
        self.api = api_client
        self._users_cache: Optional[List[Dict[str, Any]]] = None
        self._vms_cache: Optional[List[Dict[str, Any]]] = None
        self._data_fetched = False

    def fetch_all_data(self) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Récupère toutes les données nécessaires (utilisateurs et VMs) en une seule fois

        Returns:
            Tuple contenant (users, vms) ou ([], []) en cas d'erreur
        """
        if self._data_fetched:
            logger.info("Utilisation des données en cache")
            return self._users_cache or [], self._vms_cache or []

        logger.info("Début de récupération centralisée des données")

        # Récupération des utilisateurs
        try:
            self._users_cache = self.api.users.get()
            logger.info("Utilisateurs récupérés", count=len(self._users_cache))
        except UsersFetchError as e:
            logger.error("Impossible de récupérer les utilisateurs", error=str(e))
            self._users_cache = []

        # Récupération des VMs
        try:
            self._vms_cache = self.api.vms.get()
            logger.info("VMs récupérées", count=len(self._vms_cache))
        except VMsFetchError as e:
            logger.error("Impossible de récupérer les VMs", error=str(e))
            self._vms_cache = []

        self._data_fetched = True
        logger.info("Récupération centralisée des données terminée")

        return self._users_cache or [], self._vms_cache or []

    def get_users(self) -> List[Dict[str, Any]]:
        """
        Retourne les utilisateurs (doit être appelé après fetch_all_data)

        Returns:
            Liste des utilisateurs
        """
        if not self._data_fetched:
            raise RuntimeError("fetch_all_data() doit être appelé avant get_users()")
        return self._users_cache or []

    def get_vms(self) -> List[Dict[str, Any]]:
        """
        Retourne les VMs (doit être appelé après fetch_all_data)

        Returns:
            Liste des VMs
        """
        if not self._data_fetched:
            raise RuntimeError("fetch_all_data() doit être appelé avant get_vms()")
        return self._vms_cache or []

    def get_users_with_vms(self) -> List[Dict[str, Any]]:
        """
        Retourne les utilisateurs avec leurs VMs associées

        Returns:
            Liste des utilisateurs avec leurs VMs
        """
        users = self.get_users()
        vms = self.get_vms()
        
        # Associer les VMs aux utilisateurs
        self.api.users.add_vms_to_users(users, vms)
        return users

    def clear_cache(self) -> None:
        """Vide le cache des données"""
        self._users_cache = None
        self._vms_cache = None
        self._data_fetched = False
        logger.info("Cache des données vidé")

    @property
    def is_data_loaded(self) -> bool:
        """Indique si les données sont chargées"""
        return self._data_fetched
