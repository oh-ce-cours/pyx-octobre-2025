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

BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:N1uLlTBt"


users = get_users(BASE_URL)
vms = get_vms(BASE_URL)


add_vms_to_users(users, vms)

import IPython

IPython.embed()
