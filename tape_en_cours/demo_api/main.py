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
import json

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"

users = get_users(BASE_URL)
vms = get_vms(BASE_URL)
add_vms_to_users(users, vms)
json.dump(
    users,
    open("vm_users.json", "w", encoding="utf8"),
    indent=4,
    sort_keys=True,
    default=str,
)


# Récupération sécurisée des identifiants
print("=== Connexion utilisateur ===")
user_email, user_password = get_credentials(email="jean@dupont21.com")

# Tentative de création d'utilisateur, puis connexion si l'utilisateur existe déjà
token = create_user(BASE_URL, "Jean Dupont", user_email, user_password)
if not token:
    print("L'utilisateur semble déjà exister. Tentative de connexion...")
    token = login_user(BASE_URL, user_email, user_password)

user = get_logged_user_info(BASE_URL, token)
print("User info:", user)

# Le token est déjà récupéré lors de la connexion ci-dessus
if token and user:
    print("=== Création d'une VM ===")
    create_vm(
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
    print("VM créée avec succès!")
else:
    print("Erreur: Impossible de se connecter ou de récupérer les informations utilisateur")
    print("Token:", token)

# a rajouter : passage de mot de passe en CLI
# passage de varaibles en variable d'environnement
# logging
# doc
# sphinx
# jinja pour des rapports
