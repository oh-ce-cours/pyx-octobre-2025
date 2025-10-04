"""
Configuration centralisée pour demo_api

Ce module gère toutes les variables de configuration de l'application
depuis les fichiers .env et les variables d'environnement.
"""

from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os


def load_env_files() -> int:
    """
    Charge les fichiers de configuration .env dans l'ordre de priorité.

    Priorité (du plus bas au plus haut) :
    1. .env.defaults (valeurs par défaut)
    2. .env.local (configuration locale, pas dans git)
    3. .env (configuration générale)

    Returns:
        int: Nombre de fichiers .env chargés
    """
    env_files = [".env.defaults", ".env.local", ".env"]
    loaded_count = 0

    for env_file in env_files:
        if load_dotenv(env_file):
            loaded_count += 1

    return loaded_count


class Config:
    """
    Classe de configuration centralisée pour demo_api.

    Cette classe utilise python-dotenv pour charger automatiquement
    les configurations depuis les fichiers .env et les variables d'environnement.
    """

    def __init__(self):
        """Initialise la configuration en chargeant les fichiers .env"""
        self.env_files_loaded = load_env_files()

        # Configuration de l'API
        self.DEMO_API_BASE_URL = self._get_env_with_default(
            "DEMO_API_BASE_URL", "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"
        )

        # Identifiants d'authentification
        self.DEMO_API_EMAIL = self._get_env("DEMO_API_EMAIL")
        self.DEMO_API_PASSWORD = self._get_env("DEMO_API_PASSWORD")
        self.DEMO_API_TOKEN = self._get_env("DEMO_API_TOKEN")

        # Configuration du logging
        self.DEMO_API_DEBUG = self._get_env_bool("DEMO_API_DEBUG", False)
        self.DEMO_API_LOG_LEVEL = self._get_env_with_default(
            "DEMO_API_LOG_LEVEL", "INFO"
        )

        # Configuration des métadonnées
        self.DEMO_API_TIMEOUT = self._get_env_int("DEMO_API_TIMEOUT", 5)
        self.DEMO_API_MAX_RETRIES = self._get_env_int("DEMO_API_MAX_RETRIES", 3)

        # Configuration des fichiers
        self.DEMO_API_OUTPUT_FILE = self._get_env_with_default(
            "DEMO_API_OUTPUT_FILE", "output/vm_users.json"
        )

        # Validation de la configuration
        self._validate_config()
        
        # Créer le dossier de sortie s'il n'existe pas
        self._ensure_output_directory()

    def _get_env(self, key: str) -> Optional[str]:
        """Récupère une variable d'environnement optionnelle"""
        return os.environ.get(key)

    def _get_env_with_default(self, key: str, default: str) -> str:
        """Récupère une variable d'environnement avec une valeur par défaut"""
        return os.environ.get(key, default)

    def _get_env_bool(self, key: str, default: bool = False) -> bool:
        """Récupère une variable d'environnement booléenne"""
        value = os.environ.get(key, str(default))
        return value.lower() in ("true", "1", "on", "yes", "enabled")

    def _get_env_int(self, key: str, default: int) -> int:
        """Récupère une variable d'environnement entière"""
        try:
            return int(os.environ.get(key, default))
        except ValueError:
            return default

    def _get_env_list(self, key: str, default: list = None) -> list:
        """Récupère une variable d'environnement sous forme de liste"""
        if default is None:
            default = []
        value = os.environ.get(key)
        if value:
            return [item.strip() for item in value.split(",")]
        return default

    def _validate_config(self) -> None:
        """Valide la configuration chargée"""
        # Validation de l'URL de base
        if not self.DEMO_API_BASE_URL or not self.DEMO_API_BASE_URL.startswith("http"):
            raise ValueError(f"URL de base invalide: {self.DEMO_API_BASE_URL}")

        # Validation du niveau de log
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.DEMO_API_LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError(f"Niveau de log invalide: {self.DEMO_API_LOG_LEVEL}")

        # Validation des valeurs numériques
        if self.DEMO_API_TIMEOUT <= 0:
            raise ValueError(f"Timeout invalide: {self.DEMO_API_TIMEOUT}")

        if self.DEMO_API_MAX_RETRIES < 0:
            raise ValueError(f"Nombre de retry invalide: {self.DEMO_API_MAX_RETRIES}")
    
    def _ensure_output_directory(self) -> None:
        """Crée le dossier de sortie s'il n'existe pas"""
        import os
        output_dir = os.path.dirname(self.DEMO_API_OUTPUT_FILE)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

    # Propriétés de configuration pour l'accès facile
    @property
    def is_production(self) -> bool:
        """Détermine si on est en environnement de production"""
        return not self.DEMO_API_DEBUG

    @property
    def has_credentials(self) -> bool:
        """Vérifie si les identifiants sont disponibles"""
        return bool(self.DEMO_API_EMAIL and self.DEMO_API_PASSWORD)

    @property
    def has_token(self) -> bool:
        """Vérifie si un token est disponible"""
        return bool(self.DEMO_API_TOKEN)
    
    @property
    def output_directory(self) -> str:
        """Retourne le dossier de sortie"""
        import os
        return os.path.dirname(self.DEMO_API_OUTPUT_FILE)

    @property
    def auth_headers(self) -> Dict[str, str]:
        """Retourne les headers d'authentification si token disponible"""
        if self.DEMO_API_TOKEN:
            return {"Authorization": f"Bearer {self.DEMO_API_TOKEN}"}
        return {}

    @property
    def client_config(self) -> Dict[str, Any]:
        """Retourne la configuration client pour les appels API"""
        return {
            "base_url": self.DEMO_API_BASE_URL,
            "timeout": self.DEMO_API_TIMEOUT,
            "max_retries": self.DEMO_API_MAX_RETRIES,
            "ssl_verify": self.is_production,  # SSL strict en production
        }

    def to_dict(self) -> Dict[str, Any]:
        """Retourne la configuration sous forme de dictionnaire (sans les secrets)"""
        return {
            "demo_api_base_url": self.DEMO_API_BASE_URL,
            "demo_api_debug": self.DEMO_API_DEBUG,
            "demo_api_log_level": self.DEMO_API_LOG_LEVEL,
            "demo_api_timeout": self.DEMO_API_TIMEOUT,
            "demo_api_max_retries": self.DEMO_API_MAX_RETRIES,
            "demo_api_output_file": self.DEMO_API_OUTPUT_FILE,
            "demo_api_env_files_loaded": self.env_files_loaded,
            "demo_api_has_credentials": self.has_credentials,
            "demo_api_has_token": self.has_token,
            "demo_api_email_set": bool(self.DEMO_API_EMAIL),
            "demo_api_password_set": bool(self.DEMO_API_PASSWORD),
            "demo_api_token_set": bool(self.DEMO_API_TOKEN),
        }

    def __str__(self) -> str:
        """Représentation string de la configuration (sans les secrets)"""
        config_items = []
        for key, value in self.to_dict().items():
            config_items.append(f"{key}={value}")
        return f"Config({', '.join(config_items)})"

    def __repr__(self) -> str:
        """Représentation détaillée pour le debugging"""
        return f"Config(base_url='{self.DEMO_API_BASE_URL}', debug={self.DEMO_API_DEBUG}, env_files={self.env_files_loaded})"


# Instance globale de configuration
config = Config()
