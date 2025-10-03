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
import json

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"

# users = get_users(BASE_URL)
# vms = get_vms(BASE_URL)
# add_vms_to_users(users, vms)
# json.dump(
#     users,
#     open("vm_users.json", "w", encoding="utf8"),
#     indent=4,
#     sort_keys=True,
#     default=str,
# )


input()
token = create_user(BASE_URL, "Jean Dupont", "jean@dupont21.com", "motdepasse123")
if not token:
    token = login_user(BASE_URL, "jean@dupont21.com", "motdepasse123")

user = get_logged_user_info(BASE_URL, token)
print("User info:", user)

token = "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiemlwIjoiREVGIn0.fpzPuyxOU-KlOV4SBfyF4qr0VRFeDpyiVMN_xHEhQN0kMOiQ--1kYEf5hej3jv3ZjzDiFxWIAzBw3Q5bUeFlmKAzT-f1m526.kLdny7u3IbNwho9xZvGCFg.aGt3fq7Lp6E34FcXtGxFEQS6yS3j_qAotqGmpTWnCIRQYlFx7Anmd1FCHjUnqt-itgJJc5PMaRyeyNtwUDDegv-XCp8JuEbCm-63VHz8oRP3_WFehtI5qgNeXvpkXyzT5Khi59nmHJyrmPt-qTU-zfDRuHYIRTfJXTQjaBxRPNc.bi5A2LJcT7IzjbyK3GQGZs6Y7Qjd3JdZU2_U2_TCYDk"
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

print("Token:", token)

# a rajouter : passage de mot de passe en CLI
# passage de varaibles en variable d'environnement
# logging
# doc
# sphinx
