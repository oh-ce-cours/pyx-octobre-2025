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


def get_users(base_url):
    resp = requests.get(f"{base_url}/user", timeout=5)
    users = []
    for user in resp.json():
        user["created_at"] = datetime.datetime.fromtimestamp(user["created_at"] / 1e3)
        users.append(user)
    return users


def get_vms(base_url):
    resp = requests.get(f"{base_url}/vm", timeout=5)
    vms = []
    for vm in resp.json():
        vm["created_at"] = datetime.datetime.fromtimestamp(vm["created_at"] / 1e3)
        vms.append(vm)
    return vms


users = get_users(base_url)
vms = get_vms(base_url)


for user in users:
    user_id = user["id"]
    user_vms = []
    for vm in vms:
        user_vm_id = vm["user_id"]
        if user_vm_id == user_id:
            user_vms.append(vm)
    user["vms"] = user_vms

import IPython

IPython.embed()
