import requests
import datetime
from utils.logging_config import get_logger
from .decorators import retry_on_429
from .exceptions import VMsFetchError, VMCreationError, VMUpdateError, VMDeleteError

# Logger pour ce module
logger = get_logger(__name__)


def parse_unix_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts / 1e3)


@retry_on_429()
def get_vms(base_url):
    logger.info("Récupération des VMs depuis l'API", base_url=base_url)

    try:
        resp = requests.get(f"{base_url}/vm", timeout=5)
        resp.raise_for_status()

        vms = []
        for vm in resp.json():
            vm["created_at"] = parse_unix_timestamp(vm["created_at"])
            vms.append(vm)

        logger.info(
            "VMs récupérées avec succès", count=len(vms), status_code=resp.status_code
        )
        logger.debug(
            "Détails des VMs récupérées", vm_ids=[vm.get("id") for vm in vms[:5]]
        )
        return vms

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la récupération des VMs",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            base_url=base_url,
        )

        raise VMsFetchError(
            f"Impossible de récupérer les VMs depuis {base_url}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e)},
            base_url=base_url,
        )


@retry_on_429()
def create_vm(
    token,
    base_url,
    user_id,
    name,
    operating_system,
    cpu_cores,
    ram_gb,
    disk_gb,
    status="running",
):
    logger.info(
        "Création d'une nouvelle VM",
        name=name,
        user_id=user_id,
        operating_system=operating_system,
        cpu_cores=cpu_cores,
        ram_gb=ram_gb,
        disk_gb=disk_gb,
        status=status,
    )

    payload = {
        "user_id": user_id,
        "name": name,
        "operating_system": operating_system,
        "cpu_cores": cpu_cores,
        "ram_gb": ram_gb,
        "disk_gb": disk_gb,
        "status": status,
    }
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    logger.debug(
        "Payload de création VM",
        user_id=user_id,
        name=name,
        operating_system=operating_system,
        status=status,
        token_length=len(token) if token else 0,
        token_is_none=token is None,
    )

    try:
        logger.debug(f"Envoi de la requête POST vers {base_url}/vm")
        logger.debug(f"Headers: {headers}")
        logger.debug(f"Payload: {payload}")

        resp = requests.post(f"{base_url}/vm", json=payload, timeout=5, headers=headers)
        logger.debug(f"Réponse reçue - Status: {resp.status_code}")
        logger.debug(f"Headers de réponse: {dict(resp.headers)}")
        logger.debug(f"Contenu de la réponse: {resp.text[:500]}...")

        resp.raise_for_status()

        # Vérifier que la réponse n'est pas vide
        if not resp.text or resp.text.strip() == "":
            logger.error(
                "Réponse API vide pour la création de VM", status_code=resp.status_code
            )
            raise VMCreationError(
                f"Réponse API vide lors de la création de la VM '{name}' pour l'utilisateur {user_id}",
                status_code=resp.status_code,
                response_data={
                    "error": "empty_response",
                    "user_id": user_id,
                    "name": name,
                },
                user_id=user_id,
                vm_name=name,
            )

        try:
            vm_result = resp.json()
            logger.debug(
                f"Réponse JSON de l'API VM: {vm_result} (type: {type(vm_result)})"
            )
        except Exception as json_error:
            logger.error(
                "Erreur lors du parsing JSON de la réponse VM",
                json_error=str(json_error),
                response_text=resp.text[:200],
                status_code=resp.status_code,
                user_id=user_id,
                name=name,
            )
            raise VMCreationError(
                f"Erreur de parsing JSON lors de la création de la VM '{name}' pour l'utilisateur {user_id}: {str(json_error)}",
                status_code=resp.status_code,
                response_data={
                    "error": "json_parse_error",
                    "user_id": user_id,
                    "name": name,
                },
                user_id=user_id,
                vm_name=name,
            )

        # Vérifier que vm_result est valide
        if not vm_result or not isinstance(vm_result, dict):
            logger.error(
                "Réponse API invalide pour la création de VM",
                vm_result=vm_result,
                vm_result_type=type(vm_result),
                status_code=resp.status_code,
                response_text=resp.text[:200]
                if resp.text
                else "Pas de texte de réponse",
                user_id=user_id,
                name=name,
            )
            raise VMCreationError(
                f"Réponse API invalide lors de la création de la VM '{name}' pour l'utilisateur {user_id}",
                status_code=resp.status_code,
                response_data={
                    "error": "invalid_response",
                    "user_id": user_id,
                    "name": name,
                },
                user_id=user_id,
                vm_name=name,
            )

        logger.info(
            "VM créée avec succès",
            vm_id=vm_result.get("id"),
            name=name,
            user_id=user_id,
            status_code=resp.status_code,
        )
        return vm_result

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la création de la VM",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            user_id=user_id,
            name=name,
        )

        raise VMCreationError(
            f"Impossible de créer la VM '{name}' pour l'utilisateur {user_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "user_id": user_id, "name": name},
            user_id=user_id,
            vm_name=name,
        )


@retry_on_429()
def get_vm(base_url, vm_id):
    """Récupère une VM spécifique par son ID.

    Args:
        base_url (str): L'URL de base de l'API
        vm_id (int): ID de la VM

    Returns:
        dict: Données de la VM

    Raises:
        VMsFetchError: Si la récupération de la VM échoue
    """
    logger.info("Récupération d'une VM spécifique", vm_id=vm_id)

    try:
        resp = requests.get(f"{base_url}/vm/{vm_id}", timeout=5)
        resp.raise_for_status()

        vm_data = resp.json()
        vm_data["created_at"] = parse_unix_timestamp(vm_data["created_at"])

        logger.info(
            "VM récupérée avec succès",
            vm_id=vm_id,
            name=vm_data.get("name"),
            status_code=resp.status_code,
        )
        return vm_data

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la récupération de la VM",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            vm_id=vm_id,
        )

        raise VMsFetchError(
            f"Impossible de récupérer la VM {vm_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e)},
            base_url=base_url,
        )


@retry_on_429()
def update_vm(base_url, token, vm_id, updates):
    """Met à jour une VM existante.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        vm_id (int): ID de la VM
        updates (dict): Données à mettre à jour

    Returns:
        dict: Données de la VM mise à jour

    Raises:
        VMUpdateError: Si la mise à jour de la VM échoue
    """
    logger.info("Mise à jour d'une VM", vm_id=vm_id, updates_keys=list(updates.keys()))

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.patch(
            f"{base_url}/vm/{vm_id}", json=updates, headers=headers, timeout=5
        )
        resp.raise_for_status()

        vm_data = resp.json()
        logger.info(
            "VM mise à jour avec succès",
            vm_id=vm_id,
            updates_count=len(updates),
            status_code=resp.status_code,
        )
        return vm_data

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la mise à jour de la VM",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            vm_id=vm_id,
        )

        raise VMUpdateError(
            f"Impossible de mettre à jour la VM {vm_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "vm_id": vm_id},
            vm_id=vm_id,
        )


@retry_on_429()
def delete_vm(base_url, token, vm_id):
    """Supprime une VM.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        vm_id (int): ID de la VM

    Returns:
        dict: Résultat de la suppression

    Raises:
        VMDeleteError: Si la suppression de la VM échoue
    """
    logger.info("Suppression d'une VM", vm_id=vm_id)

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.delete(f"{base_url}/vm/{vm_id}", headers=headers, timeout=5)
        resp.raise_for_status()

        logger.info(
            "VM supprimée avec succès",
            vm_id=vm_id,
            status_code=resp.status_code,
        )

        # Retourner le résultat si disponible, sinon un dict vide
        try:
            return resp.json()
        except:
            return {"success": True, "vm_id": vm_id}

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la suppression de la VM",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            vm_id=vm_id,
        )

        raise VMDeleteError(
            f"Impossible de supprimer la VM {vm_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "vm_id": vm_id},
            vm_id=vm_id,
        )


@retry_on_429()
def attach_vm_to_user(base_url, token, vm_id, user_id):
    """Associe une VM à un utilisateur.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        vm_id (int): ID de la VM
        user_id (int): ID de l'utilisateur

    Returns:
        dict: Résultat de l'association

    Raises:
        VMUpdateError: Si l'association échoue
    """
    logger.info("Association VM-utilisateur", vm_id=vm_id, user_id=user_id)

    payload = {"vm_id": vm_id, "user_id": user_id}

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.post(
            f"{base_url}/Attach_VM_to_user", json=payload, headers=headers, timeout=5
        )
        resp.raise_for_status()

        logger.info(
            "VM associée avec succès à l'utilisateur",
            vm_id=vm_id,
            user_id=user_id,
            status_code=resp.status_code,
        )

        try:
            return resp.json()
        except:
            return {"success": True, "vm_id": vm_id, "user_id": user_id}

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de l'association VM-utilisateur",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            vm_id=vm_id,
            user_id=user_id,
        )

        raise VMUpdateError(
            f"Impossible d'associer la VM {vm_id} à l'utilisateur {user_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "vm_id": vm_id, "user_id": user_id},
            vm_id=vm_id,
        )


@retry_on_429()
def stop_vm(base_url, token, vm_id):
    """Arrête une VM.

    Args:
        base_url (str): L'URL de base de l'API
        token (str): Token d'authentification
        vm_id (int): ID de la VM

    Returns:
        dict: Résultat de l'arrêt

    Raises:
        VMUpdateError: Si l'arrêt de la VM échoue
    """
    logger.info("Arrêt d'une VM", vm_id=vm_id)

    payload = {"vm_id": vm_id}

    headers = {"Authorization": f"Bearer {token}"} if token else {}

    try:
        resp = requests.post(
            f"{base_url}/Stop_VM", json=payload, headers=headers, timeout=5
        )
        resp.raise_for_status()

        logger.info(
            "VM arrêtée avec succès",
            vm_id=vm_id,
            status_code=resp.status_code,
        )

        try:
            return resp.json()
        except:
            return {"success": True, "vm_id": vm_id, "action": "stopped"}

    except requests.RequestException as e:
        logger.error(
            "Erreur lors de l'arrêt de la VM",
            error=str(e),
            status_code=getattr(resp, "status_code", None),
            response_text=getattr(resp, "text", "")[:200] + "..."
            if len(getattr(resp, "text", "")) > 200
            else getattr(resp, "text", ""),
            vm_id=vm_id,
        )

        raise VMUpdateError(
            f"Impossible d'arrêter la VM {vm_id}: {str(e)}",
            status_code=getattr(resp, "status_code", None),
            response_data={"error": str(e), "vm_id": vm_id},
            vm_id=vm_id,
        )
