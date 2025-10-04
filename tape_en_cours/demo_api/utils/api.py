"""Module API unifié pour demo_api"""

from utils.api.user import get_users, add_vms_to_users
from utils.api.vm import get_vms, create_vm
from utils.api.auth import Auth

# Initialisation de l'instance Auth globale
_auth_instance = None


def _get_auth_instance(base_url):
    """Retourne l'instance Auth singleton"""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = Auth(base_url)
    return _auth_instance


# Wrapper functions pour simplifier l'utilisation
def create_user(base_url, name, email, password):
    """Crée un nouvel utilisateur"""
    auth = _get_auth_instance(base_url)
    return auth.create_user(name, email, password)


def login_user(base_url, email, password):
    """Connecte un utilisateur existant"""
    auth = _get_auth_instance(base_url)
    return auth.login_user(email, password)


def get_logged_user_info(base_url, token):
    """Récupère les informations de l'utilisateur connecté"""
    auth = _get_auth_instance(base_url)
    return auth.get_logged_user_info(token)
