import requests
import datetime
from utils.logging_config import get_logger
from .exceptions import VMsFetchError, VMCreationError, NetworkError

# Logger pour ce module
logger = get_logger(__name__)


def parse_unix_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts / 1e3)


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
        logger.debug("Détails des VMs récupérées", vm_ids=[vm.get("id") for vm in vms[:5]])
        return vms
        
    except requests.RequestException as e:
        logger.error(
            "Erreur lors de la récupération des VMs",
            error=str(e),
            status_code=getattr(resp, 'status_code', None),
            response_text=getattr(resp, 'text', '')[:200] + "..."
            if len(getattr(resp, 'text', '')) > 200
            else getattr(resp, 'text', ''),
            base_url=base_url,
        )
        
        raise VMsFetchError(
            f"Impossible de récupérer les VMs depuis {base_url}: {str(e)}",
            status_code=getattr(resp, 'status_code', None),
            response_data={"error": str(e)},
            base_url=base_url
        )


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
    headers = {"Authorization": f"Bearer {token}"}
    logger.debug(
        "Payload de création VM",
        user_id=user_id,
        name=name,
        operating_system=operating_system,
        status=status,
        token_length=len(token),
    )

    resp = requests.post(f"{base_url}/vm", json=payload, timeout=5, headers=headers)
    try:
        resp.raise_for_status()
        vm_result = resp.json()
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
            status_code=resp.status_code,
            response_text=resp.text[:200] + "..."
            if len(resp.text) > 200
            else resp.text,
            user_id=user_id,
            name=name,
        )
        return None
