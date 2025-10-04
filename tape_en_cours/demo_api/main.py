# on veut récupérer la liste des utilisateurs
# on veut récupérer la liste des VMs
# je veux les enregistrer en json
# on veut que pour un utilisateur je puisse avoir la liste de ses VMs

# on veut faire un rapport qui regroupe les VM par état (status)
# VM running: 10
# VM stopped: 5
# VM paused: 2
# ...


from utils.api import Api, create_authenticated_client
from utils.password_utils import get_or_create_token
from utils.logging_config import get_logger
from utils.config import config
import json

# Configuration du logger pour ce module
logger = get_logger(__name__)

# Initialisation du client API unifié
api = Api(config.DEMO_API_BASE_URL)

logger.info("Début de l'exécution de demo_api", base_url=api.base_url)

users = api.users.get()
logger.info("Utilisateurs récupérés", count=len(users))

vms = api.vms.get()
logger.info("VMs récupérées", count=len(vms))

api.users.add_vms_to_users(users, vms)

logger.info(
    "Sauvegarde des données utilisateurs/VMs en JSON",
    filename=config.DEMO_API_OUTPUT_FILE,
)
json.dump(
    users,
    open(config.DEMO_API_OUTPUT_FILE, "w", encoding="utf8"),
    indent=4,
    sort_keys=True,
    default=str,
)
logger.info("Sauvegarde terminée avec succès")


# Gestion intelligente des tokens d'authentification
logger.info("Début du processus d'authentification")
logger.info("Configuration chargée", config_summary=config.to_dict())

token = get_or_create_token(
    base_url=api.base_url,
    email=config.DEMO_API_EMAIL or "jean@dupont21.com",
    password=config.DEMO_API_PASSWORD,
    token_env_var="DEMO_API_TOKEN",
)

if not token:
    logger.error("Échec complet de l'authentification")
    logger.info(
        "💡 Conseil: Vérifiez que vos identifiants sont corrects dans les variables d'environnement ou la saisie interactive"
    )
else:
    # Définir le token dans le client API
    api.set_token(token)
    logger.info("Token défini dans le client API unifié")

if api.is_authenticated():
    logger.info("Récupération des informations utilisateur authentifié")
    user = api.get_user_info()
    if user:
        logger.info(
            "Informations utilisateur récupérées",
            user_id=user.get("id"),
            user_name=user.get("name"),
        )
    else:
        logger.error("Impossible de récupérer les informations utilisateur")
        user = None
else:
    logger.error("Aucun token disponible pour récupérer les informations utilisateur")
    user = None

if api.is_authenticated() and user:
    logger.info(
        "Début de création de VM",
        user_id=user["id"],
        vm_name="VM de Jean",
        operating_system="Ubuntu 22.04",
        cpu_cores=2,
        ram_gb=4,
        disk_gb=50,
    )

    vm_result = api.users.create_vm(
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
        api_authenticated=api.is_authenticated(),
        user_available=bool(user),
    )

# ✓ Implémenté : passage de mot de passe via CLI et variables d'environnement
# ✓ Implémenté : logging structuré avec structlog
# ✓ Implémenté : docstrings
# sphinx
# jinja pour des rapports
