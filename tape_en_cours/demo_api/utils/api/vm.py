import requests
import datetime
from ..logging_config import get_logger

# Logger pour ce module
logger = get_logger(__name__)


def parse_unix_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts / 1e3)


def get_vms(base_url):
    logger.info("Récupération des VMs depuis l'API", base_url=base_url)
    resp = requests.get(f"{base_url}/vm", timeout=5)
    resp.raise_for_status()

    vms = []
    for vm in resp.json():
        vm["created_at"] = parse_unix_timestamp(vm["created_at"])
        vms.append(vm)

    logger.info("VMs récupérées avec succès", count=len(vms), status_code=resp.status_code)
    logger.debug("Détails des VMs récupérées", vm_ids=[vm.get("id") for vm in vms[:5]])
    return vms


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

    resp = requests.post(f"{base_url}/vm", json=payload, timeout=5, headers=headers)
    try:
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la création de la VM: {e}")
        print(f"Payload: {payload}")
        print(f"Response: {resp.text}")
        return None
    return resp.json()
