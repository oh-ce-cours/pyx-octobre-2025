import requests
from utils.date_utils import parse_unix_timestamp
from ..logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)


def get_users(base_url):
    """Récupère la liste des utilisateurs depuis l'API.

    Args:
        base_url (str): L'URL de base de l'API

    Returns:
        list: Liste des utilisateurs avec leurs dates de création converties
    """
    logger.info("Récupération des utilisateurs depuis l'API", base_url=base_url)
    resp = requests.get(f"{base_url}/user", timeout=5)
    resp.raise_for_status()

    users = []
    for user in resp.json():
        user["created_at"] = parse_unix_timestamp(user["created_at"])
        users.append(user)

    logger.info(
        "Utilisateurs récupérés avec succès",
        count=len(users),
        status_code=resp.status_code,
    )
    logger.debug(
        "Détails des utilisateurs récupérés",
        user_ids=[user.get("id") for user in users[:5]],
    )
    return users


def add_vms_to_users(users, vms):
    """Ajoute les machines virtuelles à leurs utilisateurs respectifs.

    Args:
        users (list): Liste des utilisateurs
        vms (list): Liste des machines virtuelles

    Returns:
        None: Modifie la liste des utilisateurs en place en ajoutant les VMs
    """
    for user in users:
        user_id = user["id"]
        user_vms = []
        for vm in vms:
            user_vm_id = vm["user_id"]
            if user_vm_id == user_id:
                user_vms.append(vm)
        user["vms"] = user_vms
