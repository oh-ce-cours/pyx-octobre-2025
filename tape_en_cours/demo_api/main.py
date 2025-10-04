# on veut récupérer la liste des utilisateurs
# on veut récupérer la liste des VMs
# je veux les enregistrer en json
# on veut que pour un utilisateur je puisse avoir la liste de ses VMs

# on veut faire un rapport qui regroupe les VM par état (status)
# VM running: 10
# VM stopped: 5
# VM paused: 2
# ...


from utils.api import (
    get_users,
    get_vms,
    add_vms_to_users,
    create_user,
    login_user,
    create_vm,
    get_logged_user_info,
)
from utils.password_utils import get_credentials
from utils.logging_config import get_logger
import json

# Configuration du logger pour ce module
logger = get_logger(__name__)

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"

logger.info("Début de l'exécution de demo_api", base_url=BASE_URL)

logger.info("Récupération des utilisateurs depuis l'API")
users = get_users(BASE_URL)
logger.info("Utilisateurs récupérés", count=len(users))

logger.info("Récupération des VMs depuis l'API")
vms = get_vms(BASE_URL)
logger.info("VMs récupérées", count=len(vms))

logger.info("Association des VMs aux utilisateurs")
add_vms_to_users(users, vms)

logger.info("Sauvegarde des données utilisateurs/VMs en JSON", filename="vm_users.json")
json.dump(
    users,
    open("vm_users.json", "w", encoding="utf8"),
    indent=4,
    sort_keys=True,
    default=str,
)
logger.info("Sauvegarde terminée avec succès")


# Récupération sécurisée des identifiants
logger.info("Début du processus d'authentification")
user_email, user_password = get_credentials(email="jean@dupont21.com")
logger.info("Identifiants récupérés", email=user_email, password_source="secure_input")

# Tentative de création d'utilisateur, puis connexion si l'utilisateur existe déjà
logger.info("Tentative de création d'utilisateur", email=user_email, name="Jean Dupont")
token = create_user(BASE_URL, "Jean Dupont", user_email, user_password)
if not token:
    logger.warning(
        "Utilisateur déjà existant, tentative de connexion", email=user_email
    )
    token = login_user(BASE_URL, user_email, user_password)

logger.info("Récupération des informations utilisateur authentifié")
user = get_logged_user_info(BASE_URL, token)
logger.info(
    "Informations utilisateur récupérées",
    user_id=user.get("id"),
    user_name=user.get("name"),
)

if token and user:
    logger.info(
        "Début de création de VM",
        user_id=user["id"],
        vm_name="VM de Jean",
        operating_system="Ubuntu 22.04",
        cpu_cores=2,
        ram_gb=4,
        disk_gb=50,
    )

    vm_result = create_vm(
        token,
        BASE_URL,
        user_id=user["id"],
        name="VM de Jean",
        operating_system="Ubuntu 22.04",
        cpu_cores=2,
        ram_gb=4,
        disk_gb=50,
        status="stopped",
    )

    if vm_result:
        logger.info("VM créée avec succès", vm_id=vm_result.get("id"), status="stopped")
    else:
        logger.error("Échec de la création de VM", user_id=user["id"])
else:
    logger.error(
        "Impossible de créer la VM: authentification échouée",
        token_available=bool(token),
        user_available=bool(user),
    )

# ✓ Implémenté : passage de mot de passe via CLI et variables d'environnement
# ✓ Implémenté : logging structuré avec structlog
# doc
# sphinx
# jinja pour des rapports
