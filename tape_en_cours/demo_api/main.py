# on veut récupérer la liste des utilisateurs
# on veut récupérer la liste des VMs
# je veux les enregistrer en json
# on veut que pour un utilisateur je puisse avoir la liste de ses VMs

# on veut faire un rapport qui regroupe les VM par état (status)
# VM running: 10
# VM stopped: 5
# VM paused: 2
# ...

from typing import Optional, Dict, Any


from utils.api import Api
from utils.api.exceptions import (
    UsersFetchError,
    VMsFetchError,
    VMCreationError,
    UserInfoError,
    TokenError,
    CredentialsError,
)
from utils.password_utils import get_or_create_token
from utils.logging_config import get_logger
from utils.config import config
from reports import JSONReportGenerator

# Configuration du logger pour ce module
logger = get_logger(__name__)

# Initialisation du client API unifié
api = Api(config.DEMO_API_BASE_URL)
logger.info("Début de l'exécution de demo_api", base_url=api.base_url)

# Variables pour stocker les données
user: Optional[Dict[str, Any]] = None

try:
    users = api.users.get()
    logger.info("Utilisateurs récupérés", count=len(users))
except UsersFetchError as e:
    logger.error("Impossible de récupérer les utilisateurs", error=str(e))
    users = []

try:
    vms = api.vms.get()
    logger.info("VMs récupérées", count=len(vms))
except VMsFetchError as e:
    logger.error("Impossible de récupérer les VMs", error=str(e))
    vms = []

if users and vms:
    api.users.add_vms_to_users(users, vms)

    # Génération du rapport JSON avec le générateur dédié
    logger.info("Génération du rapport utilisateurs/VMs")
    json_generator = JSONReportGenerator()
    report_file = json_generator.generate_users_vms_report(users, "vm_users.json")
    logger.info("Rapport JSON généré avec succès", filename=report_file)
else:
    logger.warning(
        "Impossible de générer le rapport: données manquantes",
        users_count=len(users),
        vms_count=len(vms),
    )


logger.info("Début du processus d'authentification")
logger.info("Configuration chargée", config_summary=config.to_dict())

try:
    token = get_or_create_token(
        base_url=api.base_url,
        email=config.DEMO_API_EMAIL or "jean@dupont21.com",
        password=config.DEMO_API_PASSWORD,
        token_env_var="DEMO_API_TOKEN",
    )

    # Définir le token dans le client API
    api.set_token(token)
    logger.info("Token défini dans le client API unifié")

except CredentialsError as e:
    logger.error("Erreur d'authentification: identifiants invalides", error=str(e))
    logger.info(
        "💡 Conseil: Vérifiez que vos identifiants sont corrects dans les variables d'environnement ou la saisie interactive"
    )
    token = None
except TokenError as e:
    logger.error("Erreur de token", error=str(e))
    token = None

if api.is_authenticated():
    logger.info("Récupération des informations utilisateur authentifié")
    try:
        user = api.get_user_info()
        logger.info(
            "Informations utilisateur récupérées",
            user_id=user.get("id"),
            user_name=user.get("name"),
        )
    except UserInfoError as e:
        logger.error(
            "Impossible de récupérer les informations utilisateur", error=str(e)
        )
        user = None
    except TokenError as e:
        logger.error(
            "Token invalide pour récupérer les informations utilisateur", error=str(e)
        )
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

    try:
        vm_result = api.users.create_vm(
            user_id=user["id"],
            name="VM de Jean",
            operating_system="Ubuntu 22.04",
            cpu_cores=2,
            ram_gb=4,
            disk_gb=50,
            status="stopped",
        )
        logger.info("VM créée avec succès", vm_id=vm_result.get("id"), status="stopped")
    except VMCreationError as e:
        logger.error("Échec de la création de VM", error=str(e), user_id=user["id"])
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
