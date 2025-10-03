# on veut récupérer la liste des utilisateurs
# on veut récupérer la liste des VMs
# je veux les enregistrer en json
# on veut que pour un utilisateur je puisse avoir la liste de ses VMs

# on veut faire un rapport qui regroupe les VM par état (status)
# VM running: 10
# VM stopped: 5
# VM paused: 2
# ...


from utils.api import get_users, get_vms, add_vms_to_users, create_user
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

user = create_user(BASE_URL, "Jean Dupont", "jean@dupont.com", "motdepasse123")

import IPython

IPython.embed()
