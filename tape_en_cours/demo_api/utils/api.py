import requests
import datetime


def get_users(base_url):
    resp = requests.get(f"{base_url}/user", timeout=5)
    resp.raise_for_status()
    users = []
    for user in resp.json():
        user["created_at"] = datetime.datetime.fromtimestamp(user["created_at"] / 1e3)
        users.append(user)
    return users


def get_vms(base_url):
    resp = requests.get(f"{base_url}/vm", timeout=5)
    resp.raise_for_status()
    vms = []
    for vm in resp.json():
        vm["created_at"] = datetime.datetime.fromtimestamp(vm["created_at"] / 1e3)
        vms.append(vm)
    return vms


def create_user(base_url, name, email, passwor):
    resp = requests.post(
        f"{base_url}/user", json={"name": name, "email": email}, timeout=5
    )
    resp.raise_for_status()
    user = resp.json()
    user["created_at"] = datetime.datetime.fromtimestamp(user["created_at"] / 1e3)
    return user


def add_vms_to_users(users, vms):
    for user in users:
        user_id = user["id"]
        user_vms = []
        for vm in vms:
            user_vm_id = vm["user_id"]
            if user_vm_id == user_id:
                user_vms.append(vm)
        user["vms"] = user_vms
