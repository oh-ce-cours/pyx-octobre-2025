import requests
from utils.date_utils import parse_unix_timestamp
from utils.logging_config import get_logger
from utils.config import config
from .decorators import retry_on_429
from .exceptions import (
    UsersFetchError,
    UserCreationError,
    UserUpdateError,
    UserDeleteError,
)

# Logger pour ce module
logger = get_logger(__name__)


@retry_on_429()
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


@retry_on_429()
def create_user(base_url, token, name, email, password=None):
    """Crée un nouvel utilisateur via l'API.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        name (str): Nom de l'utilisateur
        email (str): Email de l'utilisateur
        password (str, optional): Mot de passe (requis pour signup)

    Returns:
        dict: Données de l'utilisateur créé

    Raises:
        UserCreationError: Si la création de l'utilisateur échoue
    """
    logger.info("Création d'un nouvel utilisateur", name=name, email=email)

    payload = {"name": name, "email": email}

    if password:
        payload["password"] = password

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.post(
            f"{base_url}/user",
            json=payload,
            headers=headers,
            timeout=config.DEMO_API_TIMEOUT,
        )
        resp.raise_for_status()

        user_data = resp.json()
        logger.debug(f"Réponse JSON de l'API: {user_data} (type: {type(user_data)})")

        # Vérifier que user_data est valide
        if not user_data or not isinstance(user_data, dict):
            logger.error(
                "Réponse API invalide pour la création d'utilisateur",
                user_data=user_data,
                user_data_type=type(user_data),
                status_code=resp.status_code,
                response_text=resp.text[:200]
                if resp.text
                else "Pas de texte de réponse",
            )
            raise UserCreationError(
                f"Réponse API invalide lors de la création de l'utilisateur '{name}' ({email})",
                status_code=resp.status_code,
                response_data={
                    "error": "invalid_response",
                    "name": name,
                    "email": email,
                },
                email=email,
            )

        logger.info(
            "Utilisateur créé avec succès",
            user_id=user_data.get("id"),
            name=name,
            email=email,
            status_code=resp.status_code,
        )
        return user_data

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la création de l'utilisateur",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            name=name,
            email=email,
        )

        raise UserCreationError(
            f"Impossible de créer l'utilisateur '{name}' ({email}): {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "name": name, "email": email},
            email=email,
        ) from e


@retry_on_429()
def get_user(base_url, user_id):
    """Récupère un utilisateur spécifique par son ID.

    Args:
        base_url (str): L'URL de base de l'API
        user_id (int): ID de l'utilisateur

    Returns:
        dict: Données de l'utilisateur

    Raises:
        UsersFetchError: Si la récupération de l'utilisateur échoue
    """
    logger.info("Récupération d'un utilisateur spécifique", user_id=user_id)

    try:
        resp = requests.get(
            f"{base_url}/user/{user_id}", timeout=config.DEMO_API_TIMEOUT
        )
        resp.raise_for_status()

        user_data = resp.json()
        user_data["created_at"] = parse_unix_timestamp(user_data["created_at"])

        logger.info(
            "Utilisateur récupéré avec succès",
            user_id=user_id,
            name=user_data.get("name"),
            status_code=resp.status_code,
        )
        return user_data

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la récupération de l'utilisateur",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            user_id=user_id,
        )

        raise UsersFetchError(
            f"Impossible de récupérer l'utilisateur {user_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e)},
            base_url=base_url,
        )


@retry_on_429()
def update_user(base_url, token, user_id, updates):
    """Met à jour un utilisateur existant.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        user_id (int): ID de l'utilisateur
        updates (dict): Données à mettre à jour

    Returns:
        dict: Données de l'utilisateur mis à jour

    Raises:
        UserUpdateError: Si la mise à jour de l'utilisateur échoue
    """
    logger.info(
        "Mise à jour d'un utilisateur",
        user_id=user_id,
        updates_keys=list(updates.keys()),
    )

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.patch(
            f"{base_url}/user/{user_id}",
            json=updates,
            headers=headers,
            timeout=config.DEMO_API_TIMEOUT,
        )
        resp.raise_for_status()

        user_data = resp.json()
        logger.info(
            "Utilisateur mis à jour avec succès",
            user_id=user_id,
            updates_count=len(updates),
            status_code=resp.status_code,
        )
        return user_data

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la mise à jour de l'utilisateur",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            user_id=user_id,
        )

        raise UserUpdateError(
            f"Impossible de mettre à jour l'utilisateur {user_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "user_id": user_id},
            user_id=user_id,
        )


@retry_on_429()
def delete_user(base_url, token, user_id):
    """Supprime un utilisateur.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        user_id (int): ID de l'utilisateur

    Returns:
        dict: Résultat de la suppression

    Raises:
        UserDeleteError: Si la suppression de l'utilisateur échoue
    """
    logger.info("Suppression d'un utilisateur", user_id=user_id)

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.delete(
            f"{base_url}/user/{user_id}",
            headers=headers,
            timeout=config.DEMO_API_TIMEOUT,
        )
        resp.raise_for_status()

        logger.info(
            "Utilisateur supprimé avec succès",
            user_id=user_id,
            status_code=resp.status_code,
        )

        # Retourner le résultat si disponible, sinon un dict vide
        try:
            return resp.json()
        except:
            return {"success": True, "user_id": user_id}

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la suppression de l'utilisateur",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            user_id=user_id,
        )

        raise UserDeleteError(
            f"Impossible de supprimer l'utilisateur {user_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "user_id": user_id},
            user_id=user_id,
        )
