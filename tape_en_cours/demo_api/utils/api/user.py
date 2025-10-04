import requests
from utils.date_utils import parse_unix_timestamp
from utils.logging_config import get_logger
from utils.config import config
from .exceptions import UsersFetchError, UserCreationError, UserUpdateError, UserDeleteError

# Logger pour ce module
logger = get_logger(__name__)


def get_users(base_url):
    """Récupère la liste des utilisateurs depuis l'API.

    Args:
        base_url (str): L'URL de base de l'API

    Returns:
        list: Liste des utilisateurs avec leurs dates de création converties

    Raises:
        UsersFetchError: Si la récupération des utilisateurs échoue
    """
    logger.info("Récupération des utilisateurs depuis l'API", base_url=base_url)

    try:
        resp = requests.get(f"{base_url}/user", timeout=config.DEMO_API_TIMEOUT)
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

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la récupération des utilisateurs",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            base_url=base_url,
        )

        raise UsersFetchError(
            f"Impossible de récupérer les utilisateurs depuis {base_url}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e)},
            base_url=base_url,
        )


def add_vms_to_users(users, vms):
    """Ajoute les machines virtuelles à leurs utilisateurs respectifs.

    Args:
        users (list): Liste des utilisateurs
        vms (list): Liste des machines virtuelles

    Returns:
        None: Modifie la liste des utilisateurs en place en ajoutant les VMs
    """
    logger.info(
        "Association des VMs aux utilisateurs", user_count=len(users), vm_count=len(vms)
    )

    association_count = 0
    for user in users:
        user_id = user["id"]
        user_vms = []
        for vm in vms:
            user_vm_id = vm["user_id"]
            if user_vm_id == user_id:
                user_vms.append(vm)
                association_count += 1
        user["vms"] = user_vms
        logger.debug(
            "VMs associées à l'utilisateur",
            user_id=user_id,
            user_name=user.get("name"),
            vm_count=len(user_vms),
        )

    logger.info(
        "Association des VMs terminée",
        total_associations=association_count,
        users_with_vms=len([u for u in users if u["vms"]]),
    )
