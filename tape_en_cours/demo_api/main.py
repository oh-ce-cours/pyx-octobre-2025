# on veut récupérer la liste des utilisateurs
# on veut récupérer la liste des VMs
# on veut que pour un utilisateur je puisse avoir la liste de ses VMs

# on veut faire un rapport qui regroupe les VM par état (status)
# VM running: 10
# VM stopped: 5
# VM paused: 2
# ...

import requests
import datetime

base_url = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"
resp = requests.get(f"{base_url}/user", timeout=5)

users = []
for user in resp.json():
    user["created_at"] = datetime.datetime.fromtimestamp(user["created_at"] / 1e3)
    users.append(user)

print(users)
